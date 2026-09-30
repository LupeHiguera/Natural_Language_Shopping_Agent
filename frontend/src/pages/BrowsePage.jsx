import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import ProductGrid from '../components/ProductGrid';
import FilterSidebar from '../components/FilterSidebar';
import { useProducts } from '../hooks/useProducts';
const keys = ['type', 'color', 'size', 'price_min', 'price_max'];
export default function BrowsePage() {
  const [params, setParams] = useSearchParams();
  const [sort, setSort] = useState('featured');
  const filters = Object.fromEntries(keys.filter(key => params.has(key)).map(key => [key, params.get(key)]));
  const invalid = filters.price_min !== undefined && filters.price_max !== undefined && Number(filters.price_min) > Number(filters.price_max);
  const { products, loading, error, retry } = useProducts(filters);
  const update = next => setParams(Object.fromEntries(Object.entries(next).filter(([, value]) => value !== '' && value != null)));
  const sorted = [...products].sort((a, b) => sort === 'price-low' ? a.price - b.price : sort === 'price-high' ? b.price - a.price : sort === 'rating' ? (b.rating ?? 0) - (a.rating ?? 0) : Number(b.featured) - Number(a.featured));
  return <div className="shell section-space"><div className="section-heading"><div><p className="eyebrow">Find your everyday favorite</p><h1 className="page-title">The collection.</h1><p className="muted" role="status">{loading ? 'Finding your pairs…' : error ? 'The catalog is temporarily unavailable.' : `${products.length} ${products.length === 1 ? 'pair' : 'pairs'} to explore`}</p></div><label className="sort-label">Sort by<select value={sort} onChange={event => setSort(event.target.value)}><option value="featured">Featured first</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option><option value="rating">Top rated</option></select></label></div>
    <div className="browse-layout"><FilterSidebar currentFilters={filters} onFilterChange={update} /><div>{Object.keys(filters).length > 0 && <div className="active-filters">{Object.entries(filters).map(([key, value]) => <button key={key} aria-label={`Remove ${key.replace('_', ' ')} filter`} onClick={() => update(Object.fromEntries(Object.entries(filters).filter(([name]) => name !== key)))}>{key.replace('_', ' ')}: {value} <span aria-hidden="true">×</span></button>)}<button className="text-link" onClick={() => update({})}>Clear all</button></div>}<ProductGrid products={sorted} loading={loading} error={invalid ? 'Maximum price must be at least the minimum price.' : error} onRetry={invalid ? undefined : retry} onReset={() => update({})} /></div></div>
  </div>;
}
