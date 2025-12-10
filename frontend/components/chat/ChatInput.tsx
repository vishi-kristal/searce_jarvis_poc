'use client';

import { useState, FormEvent } from 'react';
import { useChatStore } from '@/lib/store/chatStore';
import { sendMessage } from '@/lib/api/agent';
import { ChatMessage } from '@/lib/types/agent';

export function ChatInput() {
  const [input, setInput] = useState('');
  const {
    clientId,
    sessionId,
    isLoading,
    setLoading,
    addMessage,
    setError,
    setSessionId,
  } = useChatStore();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !clientId) {
      if (!clientId) {
        setError('Please set a Client ID first');
      }
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    const currentInput = input;
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage({
        message: currentInput,
        clientId,
        sessionId: sessionId || undefined,
      });

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        sources: response.sources,
        validation: response.validation,
        chart: response.chart,
        metadata: response.metadata,
      };

      addMessage(assistantMessage);
      setSessionId(response.sessionId);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'An unexpected error occurred';
      setError(errorMessage);
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmit(e);
              }
            }}
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder={clientId ? 'Ask a question...' : 'Please set Client ID first...'}
            rows={3}
            disabled={isLoading || !clientId}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim() || !clientId}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}

