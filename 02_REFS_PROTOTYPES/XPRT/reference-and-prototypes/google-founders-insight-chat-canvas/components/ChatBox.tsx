
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ChatMessage, MessageSender, UploadedFile } from '../types';
import { sendMessageToGemini, fileToUploadedFile, resetChat as resetGeminiChat } from '../services/geminiService';
import useVoiceRecognition from '../hooks/useVoiceRecognition';
import SendIcon from './icons/SendIcon';
import MicIcon from './icons/MicIcon';
import PaperclipIcon from './icons/PaperclipIcon';
import ChevronDownIcon from './icons/ChevronDownIcon';
import ChevronUpIcon from './icons/ChevronUpIcon';
import XMarkIcon from './icons/XMarkIcon';

interface ChatBoxProps {
  onNewArtifact: (type: string, name: string, summary: string, fullContent: string) => void;
  onNewRelationship: (sourceName: string, targetName: string, label: string) => void;
  currentArtifactNames: { name: string, type: string }[];
}

const ChatBox: React.FC<ChatBoxProps> = ({ onNewArtifact, onNewRelationship, currentArtifactNames }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [isExpanded, setIsExpanded] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<UploadedFile | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [position, setPosition] = useState({ x: 30, y: 30 });
  const [isDragging, setIsDragging] = useState(false);
  const dragStartPos = useRef({ x: 0, y: 0 });
  const chatBoxRef = useRef<HTMLDivElement>(null);

  const handleVoiceResult = useCallback((transcript: string) => {
    setInputValue(prev => prev ? `${prev} ${transcript}` : transcript);
  }, []);
  const { isListening, startListening, error: voiceError, supported: voiceSupported } = useVoiceRecognition(handleVoiceResult);

  const addMessage = useCallback((text: string, sender: MessageSender, fileInfo?: { name: string; type: string }, imageUrl?: string) => {
    setMessages(prev => [...prev, { id: Date.now().toString() + Math.random(), text, sender, timestamp: new Date(), fileInfo, imageUrl }]);
  }, []);
  
  useEffect(() => {
    addMessage(
      "Hello! I'm Insight Weaver, your AI assistant for developing startup ideas. How can I help you get started today? Feel free to ask about generating a Lean Canvas, defining your Ideal Customer Profile, or anything else!",
      MessageSender.AI
    );
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [addMessage]); // Ensure addMessage is stable or included if it changes identity

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);
  
  const handleSendMessage = async () => {
    if (!inputValue.trim() && !uploadedFile) return;
    const userMessageText = inputValue.trim();
    addMessage(userMessageText, MessageSender.USER, uploadedFile ? { name: uploadedFile.name, type: uploadedFile.type } : undefined, uploadedFile?.type.startsWith('image/') ? `data:${uploadedFile.type};base64,${uploadedFile.base64Data}` : undefined);
    
    setInputValue('');
    setIsLoading(true);
    
    const aiResponse = await sendMessageToGemini(userMessageText, uploadedFile, currentArtifactNames);
    setUploadedFile(null); // Clear uploaded file after sending
    if (fileInputRef.current) fileInputRef.current.value = "";


    // Process AI response for special tags
    let responseText = aiResponse;
    const artifactRegex = /\[ARTIFACT_GENERATED:TYPE=([^,]+),NAME=([^,]+),SUMMARY=([^\]]+)\]\s*([\s\S]*)/im;
    const relationshipRegex = /\[ARTIFACT_RELATIONSHIP:SOURCE=([^,]+),TARGET=([^,]+),LABEL=([^\]]+)\]/gim;

    let match;
    // Important: Extract full content before modifying responseText for artifact display
    let artifactsToCreate: {type: string, name: string, summary: string, fullContent: string}[] = [];
    
    // First, extract all artifact data and their full content
    responseText = responseText.replace(artifactRegex, (fullMatch, type, name, summary, content) => {
      artifactsToCreate.push({ type: type.trim(), name: name.trim(), summary: summary.trim(), fullContent: content.trim() });
      // Replace the tag with a simpler message in the chat
      return `(Artifact "${name.trim()}" of type "${type.trim()}" instruction received. It will be created on the graph.)`;
    });

    // Now process creations
    artifactsToCreate.forEach(artifact => {
      onNewArtifact(artifact.type, artifact.name, artifact.summary, artifact.fullContent);
    });
    
    // Then, process relationships
    let relationshipsToCreate: {source: string, target: string, label: string}[] = [];
    responseText = responseText.replace(relationshipRegex, (fullMatch, source, target, label) => {
      relationshipsToCreate.push({ source: source.trim(), target: target.trim(), label: label.trim() });
      return `(Relationship suggested: ${source.trim()} -> ${target.trim()} ["${label.trim()}"])`;
    });

    relationshipsToCreate.forEach(rel => {
      onNewRelationship(rel.source, rel.target, rel.label);
    });


    addMessage(responseText, MessageSender.AI);
    setIsLoading(false);
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      try {
        setIsLoading(true);
        const loadedFile = await fileToUploadedFile(file);
        setUploadedFile(loadedFile);
        addMessage(`File "${file.name}" ready for upload. Add a prompt and send.`, MessageSender.SYSTEM);
      } catch (err) {
        console.error("Error processing file:", err);
        addMessage(`Error processing file: ${file.name}.`, MessageSender.SYSTEM);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!chatBoxRef.current) return;
    // Only allow dragging if the target is the header itself, not buttons inside it
    if (e.target !== e.currentTarget && (e.target as HTMLElement).closest('button')) {
        return;
    }
    setIsDragging(true);
    const chatBoxRect = chatBoxRef.current.getBoundingClientRect();
    dragStartPos.current = {
      x: e.clientX - chatBoxRect.left,
      y: e.clientY - chatBoxRect.top,
    };
    e.preventDefault();
  };

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isDragging || !chatBoxRef.current) return;
    let newX = e.clientX - dragStartPos.current.x;
    let newY = e.clientY - dragStartPos.current.y;

    const parentWidth = window.innerWidth;
    const parentHeight = window.innerHeight;
    const boxWidth = chatBoxRef.current.offsetWidth;
    const boxHeight = chatBoxRef.current.offsetHeight;

    newX = Math.max(0, Math.min(newX, parentWidth - boxWidth));
    newY = Math.max(0, Math.min(newY, parentHeight - boxHeight));
    
    setPosition({ x: newX, y: newY });
  }, [isDragging]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    } else {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    }
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, handleMouseMove, handleMouseUp]);
  
  const handleResetChat = () => {
    setMessages([]);
    resetGeminiChat();
    addMessage("Chat session reset. How can I help you start fresh?", MessageSender.SYSTEM);
     // Re-add initial welcome message after reset
    addMessage(
      "Hello! I'm Insight Weaver, your AI assistant for developing startup ideas. How can I help you get started today? Feel free to ask about generating a Lean Canvas, defining your Ideal Customer Profile, or anything else!",
      MessageSender.AI
    );
  };

  if (!isOpen) return null;

  return (
    <div
      ref={chatBoxRef}
      className={`fixed flex flex-col shadow-2xl rounded-xl border
                  bg-slate-800/80 backdrop-blur-lg border-slate-700/70 text-white
                  transition-all duration-300 ease-in-out z-50`}
      style={{ 
        left: `${position.x}px`, 
        top: `${position.y}px`,
        width: isExpanded ? '400px' : '300px',
        height: isExpanded ? '600px' : 'auto'
      }}
      aria-label="Insight Weaver AI Chat Panel"
    >
      {/* Header */}
      <div 
        className="flex items-center justify-between p-3 bg-slate-700/50 rounded-t-xl cursor-grab select-none"
        onMouseDown={handleMouseDown}
        aria-label="Chat header, draggable"
        role="toolbar"
      >
        <h3 className="font-semibold text-sm" id="chatbox-title">Insight Weaver AI</h3>
        <div className="flex items-center space-x-2">
          <button 
            onClick={handleResetChat} 
            title="Reset Chat" 
            className="p-1 hover:bg-slate-600 rounded focus:outline-none focus:ring-1 focus:ring-pink-500"
            aria-label="Reset chat session"
          >
             <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99" />
            </svg>
          </button>
          <button 
            onClick={() => setIsExpanded(!isExpanded)} 
            className="p-1 hover:bg-slate-600 rounded focus:outline-none focus:ring-1 focus:ring-pink-500"
            aria-label={isExpanded ? "Collapse chat" : "Expand chat"}
            aria-expanded={isExpanded}
          >
            {isExpanded ? <ChevronUpIcon className="w-4 h-4" /> : <ChevronDownIcon className="w-4 h-4" />}
          </button>
          <button 
            onClick={() => setIsOpen(false)} 
            className="p-1 hover:bg-slate-600 rounded focus:outline-none focus:ring-1 focus:ring-pink-500"
            aria-label="Close chat panel"
          >
            <XMarkIcon className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Body (collapsible) */}
      {isExpanded && (
        <>
          {/* Messages Area */}
          <div 
            className="flex-grow p-3 space-y-3 overflow-y-auto min-h-[200px] scrollbar-thin scrollbar-thumb-slate-600 scrollbar-track-slate-700/50"
            aria-live="polite" 
            aria-atomic="false"
            aria-relevant="additions"
            role="log"
            aria-labelledby="chatbox-title"
          >
            {messages.map(msg => (
              <div key={msg.id} className={`flex ${msg.sender === MessageSender.USER ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-2.5 rounded-lg shadow ${msg.sender === MessageSender.USER ? 'bg-pink-600 text-white' : 'bg-slate-600 text-slate-100'}`}>
                  {msg.imageUrl && <img src={msg.imageUrl} alt={msg.fileInfo?.name || 'uploaded image'} className="max-w-xs max-h-48 rounded mb-2" />}
                  {msg.fileInfo && !msg.imageUrl && <p className="text-xs italic opacity-75 mb-1">File: {msg.fileInfo.name} ({msg.fileInfo.type})</p>}
                  <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                  <p className="text-xxs opacity-60 mt-1 text-right">{msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start" aria-label="AI is thinking">
                <div className="max-w-[80%] p-2.5 rounded-lg shadow bg-slate-600 text-slate-100 animate-pulse">
                  <p className="text-sm">Thinking...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* File Preview / Input */}
          {uploadedFile && !isLoading && (
            <div className="p-2 border-t border-slate-700 text-xs" aria-label={`File ready to send: ${uploadedFile.name}`}>
              Ready to send: <span className="font-semibold">{uploadedFile.name}</span> ({uploadedFile.type})
              <button onClick={() => { setUploadedFile(null); if(fileInputRef.current) fileInputRef.current.value = ""; }} className="ml-2 text-pink-400 hover:text-pink-300 focus:outline-none focus:underline" aria-label="Clear attached file">Clear</button>
            </div>
          )}

          {/* Input Area */}
          <div className="p-3 border-t border-slate-700/80">
            {voiceError && <p className="text-xs text-red-400 mb-1" role="alert">{voiceError}</p>}
            <div className="flex items-center space-x-2">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (handleSendMessage(), e.preventDefault())}
                placeholder="Type your message or drop a file..."
                className="flex-grow p-2.5 bg-slate-700 border border-slate-600 rounded-lg focus:ring-1 focus:ring-pink-500 focus:border-pink-500 outline-none text-sm resize-none h-10 leading-tight"
                disabled={isLoading}
                aria-label="Message input"
                rows={1}
                onInput={(e) => { // Auto-resize textarea
                    const target = e.target as HTMLTextAreaElement;
                    target.style.height = 'auto';
                    target.style.height = `${Math.min(target.scrollHeight, 120)}px`; // Max height 120px (approx 5 lines)
                }}
              />
              <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="image/*,application/pdf,.txt,.md,.csv" aria-hidden="true" tabIndex={-1} />
              <button 
                onClick={() => fileInputRef.current?.click()} 
                className="p-2.5 hover:bg-slate-700 rounded-lg disabled:opacity-50 focus:outline-none focus:ring-1 focus:ring-pink-500"
                title="Attach file"
                aria-label="Attach file"
                disabled={isLoading}
              >
                <PaperclipIcon className="w-5 h-5 text-slate-400 hover:text-pink-400" />
              </button>
              {voiceSupported && (
                <button 
                  onClick={isListening ? undefined : startListening} 
                  className={`p-2.5 hover:bg-slate-700 rounded-lg disabled:opacity-50 focus:outline-none focus:ring-1 focus:ring-pink-500 ${isListening ? 'bg-pink-600 animate-pulse' : ''}`}
                  title={isListening ? "Listening..." : "Use voice input"}
                  aria-label={isListening ? "Stop voice input, listening" : "Start voice input"}
                  aria-pressed={isListening}
                  disabled={isLoading}
                >
                  <MicIcon className={`w-5 h-5 ${isListening ? 'text-white' : 'text-slate-400 hover:text-pink-400'}`} />
                </button>
              )}
              <button 
                onClick={handleSendMessage} 
                className="p-2.5 bg-pink-600 hover:bg-pink-700 rounded-lg disabled:opacity-50 focus:outline-none focus:ring-1 focus:ring-pink-700"
                title="Send message"
                aria-label="Send message"
                disabled={isLoading || (!inputValue.trim() && !uploadedFile)}
              >
                <SendIcon className="w-5 h-5 text-white" />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatBox;
