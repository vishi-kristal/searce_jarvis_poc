import { ChatRequest, ChatResponse, NetworkError, AgentAPIError } from '@/lib/types/agent';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: { message: 'Unknown error' } }));
      throw new AgentAPIError(
        error.error?.message || `HTTP ${response.status}: ${response.statusText}`,
        `Status: ${response.status}`
      );
    }

    return response.json();
  } catch (error) {
    if (error instanceof AgentAPIError) {
      throw error;
    }
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new NetworkError('Failed to connect to server. Please check your connection.');
    }
    throw new NetworkError('An unexpected error occurred', String(error));
  }
}

export async function createSession(clientId: string, kristalId?: string) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ clientId, kristalId }),
    });

    if (!response.ok) {
      throw new AgentAPIError('Failed to create session');
    }

    return response.json();
  } catch (error) {
    if (error instanceof AgentAPIError) {
      throw error;
    }
    throw new NetworkError('Failed to create session', String(error));
  }
}

export async function* sendMessageStream(request: ChatRequest): AsyncGenerator<any, void, unknown> {
  const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new AgentAPIError('Failed to stream message');
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new NetworkError('No response body');
  }

  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            yield data;
          } catch (e) {
            // Skip invalid JSON
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

