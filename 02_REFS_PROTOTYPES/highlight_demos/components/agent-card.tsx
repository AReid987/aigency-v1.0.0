// AI Agent Card Component with Framer Motion animations
'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface AgentCardProps {
  name: string;
  description: string;
  capabilities: string[];
  avatarUrl: string;
  isActive: boolean;
  onActivate: () => void;
}

export default function AgentCard({ 
  name, 
  description, 
  capabilities, 
  avatarUrl, 
  isActive, 
  onActivate 
}: AgentCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ scale: 1.03 }}
      className="w-full max-w-sm"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Card className={`overflow-hidden border-2 ${isActive ? 'border-blue-500' : 'border-gray-200'} transition-all duration-300`}>
        <CardHeader className="relative p-0">
          <motion.div 
            className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600"
            initial={{ opacity: 0.7 }}
            animate={{ opacity: isHovered ? 0.9 : 0.7 }}
          />
          <div className="relative p-6 flex items-center gap-4">
            <motion.img 
              src={avatarUrl} 
              alt={`${name} avatar`}
              className="w-16 h-16 rounded-full border-2 border-white"
              animate={{ 
                rotate: isHovered ? 360 : 0,
              }}
              transition={{ duration: 2 }}
            />
            <div>
              <CardTitle className="text-white">{name}</CardTitle>
              <CardDescription className="text-white/80">AI Agent</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          <p className="text-gray-700 dark:text-gray-300">{description}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {capabilities.map((capability, index) => (
              <Badge key={index} variant="outline" className="bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
                {capability}
              </Badge>
            ))}
          </div>
        </CardContent>
        <CardFooter className="border-t p-6">
          <Button 
            onClick={onActivate} 
            className={`w-full ${isActive ? 'bg-green-600 hover:bg-green-700' : 'bg-blue-600 hover:bg-blue-700'}`}
          >
            {isActive ? 'Active' : 'Activate Agent'}
          </Button>
        </CardFooter>
      </Card>
    </motion.div>
  );
}
