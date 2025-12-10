'use client';

import { useState } from 'react';
import { useChatStore } from '@/lib/store/chatStore';
import { createSession } from '@/lib/api/agent';

export function SessionManager() {
  const { clientId, kristalId, setClientId, setKristalId, clearChat, setSessionId } =
    useChatStore();
  const [isCreatingSession, setIsCreatingSession] = useState(false);

  const handleNewChat = () => {
    clearChat();
    setSessionId(null);
  };

  const handleCreateSession = async () => {
    if (!clientId) {
      alert('Please enter a Client ID');
      return;
    }

    setIsCreatingSession(true);
    try {
      const session = await createSession(clientId, kristalId || undefined);
      setSessionId(session.sessionId);
    } catch (error) {
      console.error('Failed to create session:', error);
      alert('Failed to create session');
    } finally {
      setIsCreatingSession(false);
    }
  };

  return (
    <div className="bg-gray-50 border-b border-gray-200 px-4 py-3">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2">
          <label htmlFor="clientId" className="text-sm font-medium text-gray-700">
            Client ID:
          </label>
          <input
            id="clientId"
            type="text"
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            placeholder="e.g., 16325000"
            className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <label htmlFor="kristalId" className="text-sm font-medium text-gray-700">
            Kristal ID (optional):
          </label>
          <input
            id="kristalId"
            type="text"
            value={kristalId || ''}
            onChange={(e) => setKristalId(e.target.value || null)}
            placeholder="Optional"
            className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleCreateSession}
            disabled={isCreatingSession || !clientId}
            className="px-3 py-1 bg-blue-500 text-white text-sm rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isCreatingSession ? 'Creating...' : 'New Session'}
          </button>
          <button
            onClick={handleNewChat}
            className="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300"
          >
            Clear Chat
          </button>
        </div>
      </div>
    </div>
  );
}

