import { Link } from 'react-router-dom';
import Hero from '../components/Hero';
import ProductGrid from '../components/ProductGrid';
import { useFeaturedProducts } from '../hooks/useProducts';
export default function HomePage() {
  const { products, loading, error, retry } = useFeaturedProducts();
  return <>
    <Hero />
    <div className="category-strip"><div className="shell category-links"><span>A pair for every pace</span>{[['running', 'For the miles'], ['casual', 'For the everyday'], ['formal', 'For the occasion']].map(([type, label]) => <Link key={type} to={`/browse?type=${type}`}>{label}<span aria-hidden="true">↗</span></Link>)}</div></div>
    <section className="shell section-space"><div className="section-heading"><div><p className="eyebrow">A few good places to start</p><h2>The featured edit.</h2></div><Link to="/browse" className="text-link">See all shoes <span aria-hidden="true">↗</span></Link></div><ProductGrid products={products} loading={loading} error={error} onRetry={retry} /></section>
    <section className="shell discovery-note"><span className="discovery-symbol" aria-hidden="true">✳</span><div><p className="eyebrow">Shopping, in your own words</p><h2>Know the feeling.<br />Don’t know the shoe?</h2><p>Start with a style, color, size, or budget. Try “black running shoes under $100 in size 10” and let the search do the narrowing down.</p></div><a href="#shoe-search" className="button button-dark" onClick={() => document.getElementById('shoe-search')?.focus()}>Give it a try <span aria-hidden="true">↗</span></a></section>
  </>;
}
