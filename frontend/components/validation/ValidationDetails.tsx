'use client';

import { useState } from 'react';
import { ValidationResult } from '@/lib/types/agent';

interface ValidationDetailsProps {
  validation: ValidationResult;
}

export function ValidationDetails({ validation }: ValidationDetailsProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div>
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="text-xs text-gray-600 hover:text-gray-800 flex items-center gap-1"
      >
        <span>{isExpanded ? 'Hide' : 'Show'} details</span>
        <svg
          className={`w-3 h-3 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>
      {isExpanded && (
        <div className="mt-2 p-3 bg-gray-50 rounded-lg text-xs">
          <p className="text-gray-700 mb-2">
            <strong>Summary:</strong> {validation.summary}
          </p>
          <p className="text-gray-700 mb-2">
            <strong>Agent:</strong> {validation.agent}
          </p>
          {validation.discrepancies && validation.discrepancies.length > 0 && (
            <div className="mt-2">
              <strong className="text-red-700">Discrepancies:</strong>
              <ul className="list-disc list-inside mt-1 text-red-600">
                {validation.discrepancies.map((disc, index) => (
                  <li key={index}>{disc}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

