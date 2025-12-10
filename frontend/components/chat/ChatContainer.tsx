'use client';

import { useChatStore } from '@/lib/store/chatStore';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { SessionManager } from '../session/SessionManager';
import { LoadingIndicator } from './LoadingIndicator';
import { ErrorMessage } from './ErrorMessage';

export function ChatContainer() {
  const { messages, isLoading, error } = useChatStore();

  return (
    <div className="flex flex-col h-full">
      <SessionManager />
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 0 ? (
          <div className="max-w-3xl mx-auto text-center text-gray-500 mt-20">
            <h2 className="text-2xl font-semibold mb-4">Welcome to Kristal Agent PoC</h2>
            <p className="mb-6">Ask a question to get started. For example:</p>
            <div className="flex flex-wrap gap-2 justify-center">
              <button className="px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200">
                What is my portfolio value?
              </button>
              <button className="px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200">
                Show me my current holdings
              </button>
              <button className="px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200">
                What are my fees?
              </button>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} />
        )}
        {isLoading && <LoadingIndicator />}
        {error && <ErrorMessage error={error} />}
      </div>
      <ChatInput />
    </div>
  );
}

