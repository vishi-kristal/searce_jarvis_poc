'use client';

import { Source } from '@/lib/types/agent';
import { SourceLink } from './SourceLink';

interface SourceListProps {
  sources: Source[];
}

export function SourceList({ sources }: SourceListProps) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4">
      <h4 className="text-sm font-semibold text-gray-700 mb-2">Sources:</h4>
      <ul className="space-y-2">
        {sources.map((source, index) => (
          <li key={index}>
            <SourceLink source={source} />
          </li>
        ))}
      </ul>
    </div>
  );
}

