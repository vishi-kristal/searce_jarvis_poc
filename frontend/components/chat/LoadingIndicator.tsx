'use client';

export function LoadingIndicator() {
  return (
    <div className="flex justify-start mb-6">
      <div className="bg-white border border-gray-200 rounded-lg p-4 max-w-xs">
        <div className="flex items-center space-x-2">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
          <span className="text-sm text-gray-500">Agent is thinking...</span>
        </div>
      </div>
    </div>
  );
}

