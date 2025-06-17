import React, { useState, useRef, useEffect } from "react";
import { ChatMessage } from "../../types";

interface ChatInterfaceProps {
  onSendMessage: (message: string) => Promise<void>;
  isLoading?: boolean;
  messages?: ChatMessage[];
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onSendMessage,
  isLoading = false,
  messages = [],
}) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    try {
      await onSendMessage(input.trim());
      setInput("");
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full" data-oid="mdj7.5v">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4" data-oid="ln3vp4o">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
            data-oid="0hm5qw0"
          >
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.sender === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100"
              }`}
              data-oid="ql29blt"
            >
              <p className="whitespace-pre-wrap" data-oid="0yk8e:e">
                {message.content}
              </p>
              {message.diagramCode && (
                <div className="mt-2 text-xs opacity-75" data-oid="zjxs5to">
                  [Diagram Generated]
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} data-oid="qp_:67f" />
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="border-t p-4" data-oid="6u30fq.">
        <div className="flex items-end gap-2" data-oid="pku.i0a">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Describe the diagram you want to create..."
            className="flex-1 min-h-[80px] max-h-[160px] p-2 border rounded resize-none"
            disabled={isLoading}
            data-oid="sp.4al4"
          />

          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={`px-4 py-2 rounded ${
              isLoading || !input.trim()
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600 text-white"
            }`}
            data-oid="k1vwqny"
          >
            {isLoading ? "Generating..." : "Send"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
