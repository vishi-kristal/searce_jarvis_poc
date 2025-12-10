export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: Source[];
  validation?: ValidationResult;
  chart?: ChartInfo;
  metadata?: MessageMetadata;
}

export interface Source {
  type: "document" | "table" | "url";
  name: string;
  url?: string;
  query?: string; // SQL query if type is "table"
}

export interface ValidationResult {
  status: "PASS" | "FAIL";
  summary: string;
  discrepancies: string[];
  agent: string;
}

export interface ChartInfo {
  url: string;
  title: string;
}

export interface MessageMetadata {
  agentUsed: string;
  responseTime: number;
}

export interface Session {
  id: string;
  clientId: string;
  kristalId?: string;
  createdAt: Date;
  messages: ChatMessage[];
}

export interface ChatRequest {
  message: string;
  clientId: string;
  kristalId?: string;
  sessionId?: string;
}

export interface ChatResponse {
  response: string;
  sources: Source[];
  validation?: ValidationResult;
  sessionId: string;
  chart?: ChartInfo;
  metadata?: MessageMetadata;
}

export class AgentError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: string
  ) {
    super(message);
    this.name = 'AgentError';
  }
}

export class NetworkError extends AgentError {
  constructor(message: string, details?: string) {
    super(message, 'NETWORK_ERROR', details);
  }
}

export class AgentAPIError extends AgentError {
  constructor(message: string, details?: string) {
    super(message, 'AGENT_API_ERROR', details);
  }
}

