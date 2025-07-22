
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
import CodeBlock from '@/components/ui/code-block';

interface Message {
  id: number;
  sender: 'user' | 'ai';
  text: string;
  fileTree?: any;
  code?: string;
  language?: string;
  previewUrl?: string;
}

const CollaboratoryPage: React.FC = () => {
  const params = useParams();
  const projectId = params.projectId as string;
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, sender: 'ai', text: 'Welcome to the Collaboratory! How can I help you with your project?', },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentPreviewUrl, setCurrentPreviewUrl] = useState<string | null>(null);
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

      let aiResponse: Message;

      if (userMessageText.toLowerCase().includes('create web application')) {
        // Call scaffolding endpoint
        const scaffoldResponse = await fetch(`http://localhost:8000/api/projects/${projectId}/scaffold`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({ project_name: `project-${projectId}` }),
        });

        const scaffoldData = await scaffoldResponse.json();

        if (scaffoldResponse.ok) {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Project scaffolding generated successfully! Here's the structure:`, fileTree: scaffoldData.file_tree };
        } else {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Error generating scaffolding: ${scaffoldData.detail || 'An error occurred.'}` };
        }
      } else if (userMessageText.toLowerCase().includes('generate boilerplate code')) {
        // Call code generation endpoint for main.py
        const mainPyContent = `from fastapi import FastAPI\n\napp = FastAPI(\n    title=\"My App\",\n    description=\"My awesome FastAPI application\",\n    version=\"1.0.0\",\n)\n\n@app.get(\"/\")\nasync def read_root():\n    return {\"message\": \"Hello from FastAPI!\"}\n`;
        const mainPyResponse = await fetch(`http://localhost:8000/api/code-generation/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({ file_path: `/tmp/project-${projectId}/apps/api/main.py`, content: mainPyContent }),
        });

        const mainPyData = await mainPyResponse.json();

        // Call code generation endpoint for layout.tsx
        const layoutTsxContent = `import './globals.css';\n\nexport default function RootLayout({ children }: { children: React.ReactNode }) {\n  return (\n    <html lang=\"en\">\n      <body>{children}</body>\n    </html>\n  );\n}\n`;
        const layoutTsxResponse = await fetch(`http://localhost:8000/api/code-generation/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({ file_path: `/tmp/project-${projectId}/apps/web/app/layout.tsx`, content: layoutTsxContent }),
        });

        const layoutTsxData = await layoutTsxResponse.json();

        // Call code generation endpoint for page.tsx
        const pageTsxContent = `export default function Page() {\n  return ((\n    <div className=\"flex min-h-screen flex-col items-center justify-between p-24\">\n      <h1>Welcome to your new Aigency project!</h1>\n    </div>\n  ));\n}\n`;
        const pageTsxResponse = await fetch(`http://localhost:8000/api/code-generation/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`,
          },
          body: JSON.stringify({ file_path: `/tmp/project-${projectId}/apps/web/app/page.tsx`, content: pageTsxContent }),
        });

        const pageTsxData = await pageTsxResponse.json();

        if (mainPyResponse.ok && layoutTsxResponse.ok && pageTsxResponse.ok) {
          aiResponse = {
            id: messages.length + 2,
            sender: 'ai',
            text: `Boilerplate code generated successfully! You can find the files in /tmp/project-${projectId}.`,
            code: `// apps/api/main.py\n${mainPyContent}\n\n// apps/web/app/layout.tsx\n${layoutTsxContent}\n\n// apps/web/app/page.tsx\n${pageTsxContent}`,
            language: 'python' // Or 'typescript' depending on what you want to show first
          };
        } else {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Error generating boilerplate code: ${mainPyData.detail || layoutTsxData.detail || pageTsxData.detail || 'An error occurred.'}` };
        }
      } else if (userMessageText.toLowerCase().includes('preview web application')) {
        // Call preview endpoint
        const previewResponse = await fetch(`http://localhost:8000/api/projects/${projectId}/preview`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${session.access_token}`,
          },
        });

        const previewData = await previewResponse.json();

        if (previewResponse.ok) {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Preview generated successfully!`, previewUrl: previewData.preview_url };
          setCurrentPreviewUrl(previewData.preview_url);
        } else {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Error generating preview: ${previewData.detail || 'An error occurred.'}` };
        }
      } else {
        // Handle other messages (e.g., send to generic agent endpoint)
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
          aiResponse = { id: messages.length + 2, sender: 'ai', text: data.text };
        } else {
          aiResponse = { id: messages.length + 2, sender: 'ai', text: `Error: ${data.detail || 'Failed to get response from AI.'}` };
        }
      }
      setMessages((prevMessages) => [...prevMessages, aiResponse]);
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
              {msg.code && <CodeBlock language={msg.language || 'tsx'} value={msg.code} />}
              {msg.previewUrl && (
                <div className="mt-4 w-full h-96 bg-white rounded-lg overflow-hidden">
                  <iframe src={msg.previewUrl} className="w-full h-full border-none" title="Web Application Preview"></iframe>
                </div>
              )}
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
