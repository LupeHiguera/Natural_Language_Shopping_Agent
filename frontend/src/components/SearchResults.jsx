import ProductCard from './ProductCard';
export default function SearchResults({ results, loading, error, onClose, onRetry }) {
  const products = results?.products || [];
  return <section className="search-results" aria-label="Search results" aria-busy={loading}>
    <div className="results-heading"><div><p className="eyebrow">Your next pair</p><h2>{loading ? 'Finding your fit…' : error ? 'Let’s try that again' : `${products.length} ${products.length === 1 ? 'match' : 'matches'} found`}</h2></div><button className="icon-button" onClick={onClose} aria-label="Close search results">✕</button></div>
    {loading ? <div className="search-progress" role="status"><span className="spinner" />Searching the catalog…</div> : error ? <div role="alert"><p>{error}</p><button className="button button-dark mt-4" onClick={onRetry}>Try again ↗</button></div> : <>
      <p className="result-query">Results for “{results.query}”</p>
      {results.agent_response && <p className="agent-message">{results.agent_response}</p>}
      {products.length ? <div className="results-grid">{products.map(product => <ProductCard key={product.shoe_id} product={product} />)}</div> : <p className="empty-hint">Try a broader style or remove a size or price limit.</p>}
      <p className="sr-only" role="status">{products.length} search results</p>
    </>}
  </section>;
}
