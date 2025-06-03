import React from "react";

export default function ChatWindow({ messages }) {
  return (
    <div className="h-[calc(100vh-300px)] overflow-y-auto p-4 space-y-4">
      {messages.length === 0 && (
        <div className="flex items-center justify-center h-full text-gray-400 italic">
          Your journal entries will appear here...
        </div>
      )}
      {messages.map((msg, idx) => (
        <div 
          key={idx} 
          className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`
              max-w-[80%] rounded-lg px-4 py-2
              ${msg.role === "user"
                ? "bg-primary text-white"
                : "bg-gray-100 text-gray-800"
              }
            `}
          >
            {msg.content}
          </div>
        </div>
      ))}
    </div>
  );
}