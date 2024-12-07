"use client"
import SearchInput from '../components/SearchInput';
import SearchResults from '../components/SearchResults';
import { useState } from 'react';

interface SearchResult {
  id: number;
  title: string;
  description: string;
  category: string;
  similarity: number;
}

export default function Home() {
  const [results, setResults] = useState<SearchResult[]>([]);

  const handleSearch = async (query: string) => {
    const res = await fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResults(data.results);
  };

  const clearResults = () => {
    setResults([]);
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen p-4 bg-white text-black">
      <h1 className="text-3xl font-bold mb-4">Semantic Search</h1>
      <SearchInput onSearch={handleSearch} />
      <div className="mt-4 w-full flex flex-col items-center">
        {results.length > 0 && (
          <button
            onClick={clearResults}
            className="mb-4 px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg shadow-sm hover:shadow-md transition-all"
          >
            Clear Results
          </button>
        )}
        <SearchResults results={results} />
      </div>
    </main>
  );
}