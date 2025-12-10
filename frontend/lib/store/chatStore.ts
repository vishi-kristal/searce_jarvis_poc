import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { ChatMessage } from '@/lib/types/agent';

interface ChatState {
  sessionId: string | null;
  clientId: string;
  kristalId: string | null;
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;

  // Actions
  setClientId: (id: string) => void;
  setKristalId: (id: string | null) => void;
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearChat: () => void;
  setSessionId: (id: string | null) => void;
}

export const useChatStore = create<ChatState>()(
  persist(
    (set, get) => ({
      sessionId: null,
      clientId: '',
      kristalId: null,
      messages: [],
      isLoading: false,
      error: null,

      setClientId: (id) => set({ clientId: id }),
      setKristalId: (id) => set({ kristalId: id }),
      addMessage: (message) =>
        set((state) => ({
          messages: [...state.messages, message],
        })),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),
      clearChat: () =>
        set({
          messages: [],
          sessionId: null,
        }),
      setSessionId: (id) => set({ sessionId: id }),
    }),
    {
      name: 'kristal-agent-chat',
      partialize: (state) => ({
        clientId: state.clientId,
        kristalId: state.kristalId,
        sessionId: state.sessionId,
        messages: state.messages.map((msg) => ({
          ...msg,
          timestamp: msg.timestamp instanceof Date 
            ? msg.timestamp.toISOString() 
            : msg.timestamp,
        })),
      }),
      // Convert timestamp strings back to Date objects when loading from storage
      onRehydrateStorage: () => (state, error) => {
        if (error) {
          console.error('Error rehydrating chat store:', error);
          return;
        }
        if (state?.messages) {
          state.messages = state.messages.map((msg) => ({
            ...msg,
            timestamp: typeof msg.timestamp === 'string' 
              ? new Date(msg.timestamp) 
              : msg.timestamp instanceof Date 
                ? msg.timestamp 
                : new Date(),
          }));
        }
      },
    }
  )
);

