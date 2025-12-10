import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  isAuthenticated: boolean;
  user: { email: string } | null;
  login: (email: string, password: string) => boolean;
  logout: () => void;
}

// Valid credentials (for PoC - in production, this should be server-side)
const VALID_CREDENTIALS = {
  email: 'admin@kristal.ai',
  password: 'Krist@l123!',
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      user: null,

      login: (email: string, password: string) => {
        // Validate credentials
        if (
          email.toLowerCase() === VALID_CREDENTIALS.email.toLowerCase() &&
          password === VALID_CREDENTIALS.password
        ) {
          set({
            isAuthenticated: true,
            user: { email },
          });
          return true;
        }
        return false;
      },

      logout: () => {
        set({
          isAuthenticated: false,
          user: null,
        });
      },
    }),
    {
      name: 'kristal-agent-auth',
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
        user: state.user,
      }),
    }
  )
);

