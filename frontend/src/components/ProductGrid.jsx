import ProductCard from './ProductCard';
export default function ProductGrid({ products = [], loading, error, onRetry, onReset }) {
  if (loading) return <div className="product-grid" aria-label="Loading products" aria-busy="true">{Array.from({ length: 4 }, (_, i) => <div className="product-skeleton" key={i}><div /><span /><span /></div>)}<p className="sr-only" role="status">Loading products…</p></div>;
  if (error) return <div className="catalog-state" role="alert"><span aria-hidden="true">↗</span><h3>A small detour.</h3><p>{error}</p>{onRetry && <button className="button button-dark" onClick={onRetry}>Try again ↗</button>}</div>;
  if (!products.length) return <div className="catalog-state"><span aria-hidden="true">⌕</span><h3>No pairs found. Yet.</h3><p>Try a different style, color, size, or budget.</p>{onReset && <button className="button button-dark" onClick={onReset}>Reset filters ↗</button>}</div>;
  return <div className="product-grid">{products.map(product => <ProductCard key={product.shoe_id} product={product} />)}</div>;
}
