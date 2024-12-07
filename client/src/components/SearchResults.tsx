import React from 'react';

interface SearchResult {
  id: number;
  title: string;
  description: string;
  category: string;
  similarity: number;
}

interface SearchResultsProps {
  results: SearchResult[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  return (
    <div className="w-full max-w-md mt-4 mx-auto">
      {results.length > 0 ? (
        results.map((result) => (
          <div
            key={result.id}
            className="p-4 border rounded-lg shadow-sm mb-4 bg-white hover:shadow-md transition-shadow duration-200"
          >
            <h3 className="font-bold text-lg text-blue-600">{result.title}</h3>
            <p className="text-gray-700 mt-2">{result.description}</p>
            <p className="text-sm text-gray-500 mt-2">Category: {result.category}</p>
            <p className="text-sm text-gray-500 mt-1">
              Similarity: {result.similarity.toFixed(2)}
            </p>
          </div>
        ))
      ) : (
        <p className="text-gray-500 text-center">No results found.</p>
      )}
    </div>
  );
};

export default SearchResults;