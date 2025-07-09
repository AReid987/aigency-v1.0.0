"use client";

import { useState } from "react";
import AgentCard from "@/components/agent-card";

export default function Home() {
  const [activeAgent, setActiveAgent] = useState<string | null>(null);

  const agents = [
    {
      id: "assistant",
      name: "AI Assistant",
      description:
        "A helpful AI assistant that can answer questions, provide information, and help with various tasks.",
      capabilities: ["Q&A", "Research", "Writing", "Analysis"],
      avatarUrl:
        "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=100&h=100&fit=crop&crop=face",
    },
    {
      id: "coder",
      name: "Code Expert",
      description:
        "Specialized in programming, code review, debugging, and software development best practices.",
      capabilities: ["Coding", "Debugging", "Code Review", "Architecture"],
      avatarUrl:
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=100&h=100&fit=crop&crop=face",
    },
    {
      id: "creative",
      name: "Creative Writer",
      description:
        "Expert in creative writing, storytelling, content creation, and artistic expression.",
      capabilities: ["Writing", "Storytelling", "Content", "Creativity"],
      avatarUrl:
        "https://images.unsplash.com/photo-1552058544-f2b08422138a?w=100&h=100&fit=crop&crop=face",
    },
  ];

  const handleActivateAgent = (agentId: string) => {
    setActiveAgent(activeAgent === agentId ? null : agentId);
  };

  return (
    <div className='min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8'>
      <div className='max-w-7xl mx-auto'>
        <div className='text-center mb-12'>
          <h1 className='text-4xl font-bold text-gray-900 dark:text-white mb-4'>
            AI Agent Dashboard
          </h1>
          <p className='text-lg text-gray-600 dark:text-gray-300'>
            Choose an AI agent to assist you with your tasks
          </p>
        </div>

        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 justify-items-center'>
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              name={agent.name}
              description={agent.description}
              capabilities={agent.capabilities}
              avatarUrl={agent.avatarUrl}
              isActive={activeAgent === agent.id}
              onActivate={() => handleActivateAgent(agent.id)}
            />
          ))}
        </div>

        {activeAgent && (
          <div className='mt-12 text-center'>
            <div className='bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg max-w-md mx-auto'>
              <h3 className='text-xl font-semibold text-gray-900 dark:text-white mb-2'>
                Agent Activated!
              </h3>
              <p className='text-gray-600 dark:text-gray-300'>
                {agents.find((a) => a.id === activeAgent)?.name} is now ready to
                assist you.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
