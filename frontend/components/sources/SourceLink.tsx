'use client';

import { Source } from '@/lib/types/agent';

interface SourceLinkProps {
  source: Source;
}

export function SourceLink({ source }: SourceLinkProps) {
  const getIcon = () => {
    switch (source.type) {
      case 'document':
        return '📄';
      case 'table':
        return '📊';
      case 'url':
        return '🔗';
      default:
        return '📄';
    }
  };

  if (source.url) {
    return (
      <a
        href={source.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm text-blue-600 hover:text-blue-800 underline flex items-center gap-2"
      >
        <span>{getIcon()}</span>
        <span>{source.name}</span>
        <svg
          className="w-3 h-3"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
          />
        </svg>
      </a>
    );
  }

  return (
    <div className="text-sm text-gray-600 flex items-center gap-2">
      <span>{getIcon()}</span>
      <span>{source.name}</span>
      {source.query && (
        <details className="ml-2">
          <summary className="cursor-pointer text-xs text-gray-500">View Query</summary>
          <pre className="mt-2 p-2 bg-gray-100 rounded text-xs overflow-x-auto">
            {source.query}
          </pre>
        </details>
      )}
    </div>
  );
}

