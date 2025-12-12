import { useState } from 'react';
import { useAISearch } from '../hooks/useAISearch';
import SearchResults from './SearchResults';

const AISearchBar = () => {
  const [query, setQuery] = useState('');
  const { results, loading, error, search, clearResults } = useAISearch();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      search(query);
    }
  };

  const handleClear = () => {
    setQuery('');
    clearResults();
  };

  return (
    <div className="relative">
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex items-center">
          <div className="relative flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try: 'red running shoes under $100 in size 10'"
              className="w-full px-4 py-3 pr-24 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition"
            />
            {query && (
              <button
                type="button"
                onClick={handleClear}
                className="absolute right-16 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="ml-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Searching...
              </span>
            ) : (
              'Search'
            )}
          </button>
        </div>
      </form>

      {/* Results Panel */}
      {(results || error) && (
        <SearchResults
          results={results}
          error={error}
          onClose={handleClear}
        />
      )}
    </div>
  );
};

export default AISearchBar;