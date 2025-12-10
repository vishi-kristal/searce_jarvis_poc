'use client';

import { ChatMessage } from '@/lib/types/agent';
import { SourceList } from '../sources/SourceList';
import { ValidationBadge } from '../validation/ValidationBadge';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Image from 'next/image';

interface MessageBubbleProps {
  message: ChatMessage;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  
  // Handle timestamp - can be Date object or string (from localStorage)
  const getTimestamp = () => {
    if (message.timestamp instanceof Date) {
      return message.timestamp.toLocaleTimeString();
    }
    if (typeof message.timestamp === 'string') {
      return new Date(message.timestamp).toLocaleTimeString();
    }
    return new Date().toLocaleTimeString();
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div
        className={`max-w-3xl rounded-lg p-4 ${
          isUser
            ? 'bg-blue-500 text-white'
            : 'bg-white border border-gray-200 text-gray-900'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <SourceList sources={message.sources} />
          </div>
        )}

        {message.validation && (
          <div className="mt-4">
            <ValidationBadge validation={message.validation} />
          </div>
        )}

        {message.chart && (
          <div className="mt-4">
            <Image
              src={message.chart.url}
              alt={message.chart.title}
              width={800}
              height={400}
              className="rounded-lg"
            />
          </div>
        )}

        <div className={`text-xs mt-2 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
          {getTimestamp()}
        </div>
      </div>
    </div>
  );
}

