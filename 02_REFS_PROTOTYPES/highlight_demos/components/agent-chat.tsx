'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  model?: string;
  provider?: string;
}

interface AgentConfig {
  id: string;
  name: string;
  type: string;
  description: string;
  capabilities: string[];
  preferredProvider?: string;
  preferredModel?: string;
}

interface AgentChatProps {
  agentId?: string;
  userId?: string;
  sessionId?: string;
  onSessionCreate?: (sessionId: string) => void;
}

export default function AgentChat({
  agentId = 'assistant',
  userId = 'user_123',
  sessionId: initialSessionId,
  onSessionCreate
}: AgentChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(initialSessionId || null);
  const [availableAgents, setAvailableAgents] = useState<AgentConfig[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>(agentId);
  const [providers, setProviders] = useState<any[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load available agents and providers
  useEffect(() => {
    loadAgentsAndProviders();
  }, []);

  // Load session history if sessionId provided
  useEffect(() => {
    if (sessionId) {
      loadSessionHistory();
    }
  }, [sessionId]);

  // Auto-scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadAgentsAndProviders = async () => {
    try {
      const [agentsRes, providersRes] = await Promise.all([
        fetch('/api/agents/chat?action=agents'),
        fetch('/api/agents/chat?action=providers')
      ]);

      if (agentsRes.ok) {
        const { agents } = await agentsRes.json();
        setAvailableAgents(agents);
      }

      if (providersRes.ok) {
        const { providers } = await providersRes.json();
        setProviders(providers);
      }
    } catch (error) {
      console.error('Failed to load agents/providers:', error);
    }
  };

  const loadSessionHistory = async () => {
    if (!sessionId) return;

    try {
      const response = await fetch(`/api/agents/chat?action=session&sessionId=${sessionId}`);
      if (response.ok) {
        const { history } = await response.json();
        const formattedMessages = history.map((msg: any) => ({
          ...msg,
          timestamp: new Date()
        }));
        setMessages(formattedMessages);
      }
    } catch (error) {
      console.error('Failed to load session history:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/agents/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          sessionId,
          message: inputMessage,
          agentId: selectedAgent,
          userId,
          options: {
            temperature: 0.7,
            maxTokens: 1000
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      // Update session ID if new session was created
      if (data.sessionId && !sessionId) {
        setSessionId(data.sessionId);
        onSessionCreate?.(data.sessionId);
      }

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
        model: data.model,
        provider: data.provider
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Error sending message:', error);

      let errorContent = 'Sorry, I encountered an error processing your message.';

      if (error instanceof Error) {
        if (error.message.includes('Failed to send message')) {
          errorContent = 'Failed to connect to AI service. Please check your internet connection and try again.';
        } else if (error.message.includes('No AI providers')) {
          errorContent = 'No AI providers are currently available. Please check the system configuration.';
        } else {
          errorContent = `Error: ${error.message}`;
        }
      }

      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: errorContent,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const selectedAgentConfig = availableAgents.find(agent => agent.id === selectedAgent);

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <Card className="mb-4">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                🤖 AI Agent Chat
                {selectedAgentConfig && (
                  <Badge variant="secondary">{selectedAgentConfig.name}</Badge>
                )}
              </CardTitle>
              <CardDescription>
                {selectedAgentConfig?.description || 'Chat with AI agents using your configured providers'}
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={clearChat}>
                Clear Chat
              </Button>
            </div>
          </div>

          {/* Agent Selection */}
          <div className="flex flex-wrap gap-2 mt-3">
            {availableAgents.map(agent => (
              <Button
                key={agent.id}
                variant={selectedAgent === agent.id ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedAgent(agent.id)}
              >
                {agent.name}
              </Button>
            ))}
          </div>

          {/* Provider Status */}
          {providers.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Providers:</span>
              {providers.map(provider => (
                <Badge
                  key={provider.id}
                  variant={provider.available ? 'default' : 'secondary'}
                  className="text-xs"
                >
                  {provider.name} ({provider.models})
                </Badge>
              ))}
            </div>
          )}
        </CardHeader>
      </Card>

      {/* Chat Messages */}
      <Card className="flex-1 flex flex-col">
        <CardContent className="flex-1 flex flex-col p-4">
          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 dark:text-gray-400 py-8">
                <div className="text-4xl mb-2">💬</div>
                <p>Start a conversation with the AI agent!</p>
                {selectedAgentConfig && (
                  <div className="mt-4 text-sm">
                    <p><strong>Capabilities:</strong></p>
                    <div className="flex flex-wrap gap-1 justify-center mt-2">
                      {selectedAgentConfig.capabilities.map(cap => (
                        <Badge key={cap} variant="outline" className="text-xs">
                          {cap}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className="text-xs opacity-70 mt-1 flex items-center gap-2">
                      <span>{message.timestamp.toLocaleTimeString()}</span>
                      {message.model && (
                        <Badge variant="outline" className="text-xs">
                          {message.provider}/{message.model.split('/').pop()}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-2">
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                    <span className="text-gray-600 dark:text-gray-400">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="flex gap-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
              className="flex-1 min-h-[60px] max-h-[120px] px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="px-6"
            >
              Send
            </Button>
          </div>

          {/* Session Info */}
          {sessionId && (
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
              Session: {sessionId}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
