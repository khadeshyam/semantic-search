"use client"
import { useState, useCallback, useRef } from 'react';
import debounce from 'lodash/debounce';

interface SearchInputProps {
  onSearch: (query: string, signal: AbortSignal) => void;
}

const SearchInput: React.FC<SearchInputProps> = ({ onSearch }) => {
  const [query, setQuery] = useState<string>('');
  const abortControllerRef = useRef<AbortController | null>(null);

  const debouncedSearch = useCallback(
    debounce((query: string) => {
      if (query.trim()) {
        if (abortControllerRef.current) {
          abortControllerRef.current.abort();
        }
        const newAbortController = new AbortController();
        abortControllerRef.current = newAbortController;
        onSearch(query, newAbortController.signal);
      }
    }, 750),
    [onSearch]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newQuery = e.target.value;
    setQuery(newQuery);
    debouncedSearch(newQuery);
  };

  const handleSearchClick = () => {
    if (query.trim()) {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      const newAbortController = new AbortController();
      abortControllerRef.current = newAbortController;
      onSearch(query, newAbortController.signal);
    }
  };

  return (
    <div className="w-full max-w-md flex items-center space-x-2">
      <input
        type="text"
        value={query}
        onChange={handleInputChange}
        placeholder="Search posts..."
        className="flex-1 px-4 py-2 border rounded-lg shadow-sm"
      />
      <button
        onClick={handleSearchClick}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md"
      >
        Search
      </button>
    </div>
  );
};

export default SearchInput;