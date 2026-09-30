import { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAISearch } from '../hooks/useAISearch';
import SearchResults from './SearchResults';

const examples = ['Running shoes under $100', 'Black shoes in size 10', 'Casual sneakers'];
export default function AISearchBar() {
  const [query, setQuery] = useState('');
  const { results, loading, error, search, clearResults } = useAISearch();
  const root = useRef(null);
  const input = useRef(null);
  const location = useLocation();
  useEffect(() => { clearResults(); }, [location, clearResults]);
  useEffect(() => {
    const outside = event => { if (!root.current?.contains(event.target)) clearResults(); };
    document.addEventListener('pointerdown', outside);
    return () => document.removeEventListener('pointerdown', outside);
  }, [clearResults]);
  const close = () => { clearResults(); input.current?.focus(); };
  const submit = event => { event.preventDefault(); search(query); };
  return <div ref={root} className="search-container" onKeyDown={event => { if (event.key === 'Escape') close(); }}>
    <form className="search-form" role="search" onSubmit={submit}>
      <span className="search-spark" aria-hidden="true">✳</span>
      <label className="sr-only" htmlFor="shoe-search">Describe the shoes you want</label>
      <input id="shoe-search" ref={input} type="search" value={query} maxLength={200} onChange={event => { setQuery(event.target.value); clearResults(); }} placeholder="Describe your next pair. We'll find the fit." aria-describedby="search-hint" />
      {query && <button type="button" className="clear-search" aria-label="Clear search" onClick={() => { setQuery(''); close(); }}>✕</button>}
      <button className="button button-dark search-submit" type="submit" disabled={loading || !query.trim()}>{loading ? 'Searching…' : 'Find my pair'}<span aria-hidden="true">↗</span></button>
    </form>
    <div className="search-hints" id="search-hint"><span>Try a little detail:</span>{examples.map(example => <button key={example} type="button" onClick={() => { setQuery(example); search(example); }}>{example}<span aria-hidden="true">↗</span></button>)}</div>
    {loading && <p className="sr-only" role="status">Searching the catalog…</p>}
    {(results || error || loading) && <SearchResults results={results} loading={loading} error={error} onClose={close} onRetry={() => search(query)} />}
  </div>;
}
