'use client';

import { ValidationResult } from '@/lib/types/agent';
import { ValidationDetails } from './ValidationDetails';

interface ValidationBadgeProps {
  validation: ValidationResult;
}

export function ValidationBadge({ validation }: ValidationBadgeProps) {
  const isPass = validation.status === 'PASS';

  return (
    <div className="mt-4 pt-4 border-t border-gray-200">
      <div className="flex items-center gap-2 mb-2">
        {isPass ? (
          <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
        ) : (
          <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clipRule="evenodd"
            />
          </svg>
        )}
        <span
          className={`text-sm font-semibold ${
            isPass ? 'text-green-700' : 'text-red-700'
          }`}
        >
          Validation: {validation.status}
        </span>
      </div>
      <ValidationDetails validation={validation} />
    </div>
  );
}

