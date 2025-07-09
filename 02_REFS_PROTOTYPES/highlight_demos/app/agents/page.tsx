"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import AgentChat from "@/components/agent-chat";

export default function AgentsPage() {
  const [activeSession, setActiveSession] = useState<string | null>(null);
  const [selectedAgent, setSelectedAgent] = useState<string>("assistant");

  const agentTypes = [
    {
      id: "assistant",
      name: "AI Assistant",
      icon: "🤖",
      description: "General-purpose AI assistant for questions and tasks",
      capabilities: ["General Knowledge", "Problem Solving", "Task Assistance"],
      provider: "OpenRouter (Claude 3.5 Sonnet)",
    },
    {
      id: "researcher",
      name: "Research Agent",
      icon: "🔬",
      description:
        "Specialized in research, analysis, and information synthesis",
      capabilities: [
        "Literature Review",
        "Data Analysis",
        "Research Methodology",
      ],
      provider: "Google (Gemini 1.5 Pro)",
    },
    {
      id: "coder",
      name: "Code Agent",
      icon: "💻",
      description:
        "Expert in programming, code review, and software development",
      capabilities: ["Code Generation", "Debugging", "Architecture Design"],
      provider: "Groq (Llama 3.1 70B)",
    },
    {
      id: "analyst",
      name: "Data Analyst",
      icon: "📊",
      description: "Specialized in data analysis, visualization, and insights",
      capabilities: [
        "Statistical Analysis",
        "Data Visualization",
        "Business Intelligence",
      ],
      provider: "Cerebras (Llama 3.1 70B)",
    },
    {
      id: "creative",
      name: "Creative Agent",
      icon: "🎨",
      description: "Creative writing, brainstorming, and content creation",
      capabilities: ["Creative Writing", "Brainstorming", "Content Strategy"],
      provider: "Chutes (Claude 3.5 Sonnet)",
    },
    {
      id: "multilingual",
      name: "Multilingual Agent",
      icon: "🌍",
      description:
        "Translation, multilingual content, and cross-cultural communication",
      capabilities: ["Translation", "Localization", "Cultural Adaptation"],
      provider: "Mistral (Mistral Large)",
    },
  ];

  const handleSessionCreate = (sessionId: string) => {
    setActiveSession(sessionId);
  };

  const startNewChat = (agentId: string) => {
    setSelectedAgent(agentId);
    setActiveSession(null);
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800'>
      {/* Header */}
      <div className='p-8 pb-4'>
        <div className='max-w-7xl mx-auto'>
          <div className='text-center mb-8'>
            <h1 className='text-4xl font-bold text-gray-900 dark:text-white mb-4'>
              🤖 AI Agent Network
            </h1>
            <p className='text-lg text-gray-600 dark:text-gray-300 mb-6'>
              Chat with specialized AI agents powered by your configured
              providers
            </p>

            {/* Provider Status */}
            <div className='flex justify-center gap-2 mb-6'>
              <Badge variant='default' className='bg-green-500'>
                🔗 OpenRouter
              </Badge>
              <Badge variant='default' className='bg-blue-500'>
                🔗 Google Gemini
              </Badge>
              <Badge variant='default' className='bg-orange-500'>
                🔗 Groq
              </Badge>
              <Badge variant='default' className='bg-purple-500'>
                🔗 Cerebras
              </Badge>
              <Badge variant='default' className='bg-pink-500'>
                🔗 Chutes
              </Badge>
              <Badge variant='default' className='bg-indigo-500'>
                🔗 Mistral
              </Badge>
            </div>
          </div>

          {/* Agent Selection Grid */}
          <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8'>
            {agentTypes.map((agent) => (
              <Card
                key={agent.id}
                className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                  selectedAgent === agent.id
                    ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20"
                    : "hover:shadow-md"
                }`}
                onClick={() => startNewChat(agent.id)}
              >
                <CardHeader className='pb-3'>
                  <div className='text-center'>
                    <div className='text-3xl mb-2'>{agent.icon}</div>
                    <CardTitle className='text-lg'>{agent.name}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className='pt-0'>
                  <CardDescription className='text-center text-sm mb-3'>
                    {agent.description}
                  </CardDescription>

                  <div className='space-y-2'>
                    <div className='text-xs font-medium text-gray-600 dark:text-gray-400'>
                      Capabilities:
                    </div>
                    <div className='flex flex-wrap gap-1'>
                      {agent.capabilities.map((cap) => (
                        <Badge key={cap} variant='outline' className='text-xs'>
                          {cap}
                        </Badge>
                      ))}
                    </div>

                    <div className='text-xs text-gray-500 dark:text-gray-400 mt-2'>
                      <strong>Provider:</strong> {agent.provider}
                    </div>
                  </div>

                  <Button
                    className='w-full mt-3'
                    size='sm'
                    variant={selectedAgent === agent.id ? "default" : "outline"}
                  >
                    {selectedAgent === agent.id ? "Selected" : "Select Agent"}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <div className='px-8 pb-8 relative z-10'>
        <div className='max-w-7xl mx-auto'>
          <Card className='relative z-10 shadow-lg'>
            <CardContent className='p-6' style={{ height: "600px" }}>
              <AgentChat
                agentId={selectedAgent}
                userId='user_123'
                sessionId={activeSession}
                onSessionCreate={handleSessionCreate}
              />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Features Info */}
      <div className='px-8 pb-8 relative z-0'>
        <div className='max-w-7xl mx-auto'>
          <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
            {/* AI Providers */}
            <Card>
              <CardHeader>
                <CardTitle>🔗 AI Provider Network</CardTitle>
                <CardDescription>
                  Multiple AI providers for diverse capabilities
                </CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'>
                <div className='space-y-3'>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-green-500'>OpenRouter</Badge>
                    <span className='text-sm'>
                      Access to Claude, GPT-4, Llama models
                    </span>
                  </div>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-blue-500'>Google Gemini</Badge>
                    <span className='text-sm'>
                      Long-context understanding, multimodal
                    </span>
                  </div>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-orange-500'>Groq</Badge>
                    <span className='text-sm'>
                      Ultra-fast inference, Llama models
                    </span>
                  </div>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-purple-500'>Cerebras</Badge>
                    <span className='text-sm'>
                      Fastest AI inference available
                    </span>
                  </div>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-pink-500'>Chutes</Badge>
                    <span className='text-sm'>
                      Premium model access and routing
                    </span>
                  </div>
                  <div className='flex items-center gap-3'>
                    <Badge className='bg-indigo-500'>Mistral</Badge>
                    <span className='text-sm'>
                      European AI, multilingual, privacy-focused
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Features */}
            <Card>
              <CardHeader>
                <CardTitle>✨ Advanced Features</CardTitle>
                <CardDescription>
                  Intelligent agent system with specialized capabilities
                </CardDescription>
              </CardHeader>
              <CardContent className='space-y-4'>
                <div className='space-y-3'>
                  <div className='flex items-start gap-3'>
                    <div className='w-2 h-2 bg-blue-500 rounded-full mt-2'></div>
                    <div>
                      <p className='font-medium'>Specialized Agents</p>
                      <p className='text-sm text-gray-600 dark:text-gray-300'>
                        Each agent optimized for specific tasks and use cases
                      </p>
                    </div>
                  </div>

                  <div className='flex items-start gap-3'>
                    <div className='w-2 h-2 bg-green-500 rounded-full mt-2'></div>
                    <div>
                      <p className='font-medium'>Provider Optimization</p>
                      <p className='text-sm text-gray-600 dark:text-gray-300'>
                        Automatic selection of best provider for each task
                      </p>
                    </div>
                  </div>

                  <div className='flex items-start gap-3'>
                    <div className='w-2 h-2 bg-purple-500 rounded-full mt-2'></div>
                    <div>
                      <p className='font-medium'>Session Management</p>
                      <p className='text-sm text-gray-600 dark:text-gray-300'>
                        Persistent conversations with context awareness
                      </p>
                    </div>
                  </div>

                  <div className='flex items-start gap-3'>
                    <div className='w-2 h-2 bg-orange-500 rounded-full mt-2'></div>
                    <div>
                      <p className='font-medium'>Real-time Responses</p>
                      <p className='text-sm text-gray-600 dark:text-gray-300'>
                        Fast, streaming responses with usage tracking
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
