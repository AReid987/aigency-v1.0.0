
'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { Send, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
// import { createClientComponentClient } from '@supabase/ssr';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import FileTree from '@/components/ui/file-tree';

interface Message {
  id: number;
  sender: 'user' | 'ai';
  text: string;
  fileTree?: any;
}

const CollaboratoryPage: React.FC = () => {
  const params = useParams();
  const projectId = params.projectId as string;
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, sender: 'ai', text: 'Welcome to the Collaboratory! How can I help you with your project?', },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // const supabase = createClientComponentClient();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (event: React.FormEvent) => {
    event.preventDefault();
    if (inputMessage.trim() === '' || isLoading) return;

    const userMessageText = inputMessage;
    const newMessage: Message = { id: messages.length + 1, sender: 'user', text: userMessageText };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // const { data: { session } } = await supabase.auth.getSession();
      const session = { access_token: "" }; // Placeholder
      if (!session) {
        setMessages((prevMessages) => [...prevMessages, { id: prevMessages.length + 1, sender: 'ai', text: 'Please log in to send messages.' }]);
        setIsLoading(false);
        return;
      }

      const response = await fetch(`http://localhost:8000/api/agent/respond`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ text: userMessageText }),
      });

        const data = await response.json();

        if (response.ok) {
          const aiResponse: Message = { id: messages.length + 2, sender: 'ai', text: data.text, fileTree: data.file_tree };
          setMessages((prevMessages) => [...prevMessages, aiResponse]);
        } else {
          const errorResponse: Message = { id: messages.length + 2, sender: 'ai', text: `Error: ${data.detail || 'Failed to get response from AI.'}` };
          setMessages((prevMessages) => [...prevMessages, errorResponse]);
        }
      }
    } catch (error) {
      const errorResponse: Message = { id: messages.length + 2, sender: 'ai', text: 'An unexpected error occurred. Please try again.' };
      setMessages((prevMessages) => [...prevMessages, errorResponse]);
    }

    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-screen bg-[#141313] text-white">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex-1 overflow-y-auto p-4 space-y-4"
      >
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`max-w-md px-4 py-2 rounded-lg ${msg.sender === 'user' ? 'bg-[#615EFF]' : 'bg-[#1F1F1F]'}`}
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.text}
              </ReactMarkdown>
              {msg.fileTree && <FileTree fileTree={msg.fileTree} />}
              {msg.fileTree && (
                <div className="flex space-x-2 mt-2">
                  <Button className="bg-green-500 hover:bg-green-600">Approve</Button>
                  <Button className="bg-red-500 hover:bg-red-600">Request Changes</Button>
                </div>
              )}
            </motion.div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </motion.div>

      <motion.form
        onSubmit={handleSendMessage}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="p-4 border-t border-gray-700 flex items-center space-x-2"
      >
        <Input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 bg-[#1F1F1F] text-white border-gray-600 focus:ring-[#615EFF]"
          disabled={isLoading}
        />
        <Button type="submit" disabled={isLoading} className="bg-[#615EFF] hover:bg-[#4E4AFF]">
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </motion.form>
    </div>
  );
};

export default CollaboratoryPage;
