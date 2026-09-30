import { Link } from 'react-router-dom';
import ProductImage from './ProductImage';
export default function ProductCard({ product }) {
  return <article className="product-card"><Link to={`/product/${product.shoe_id}`} className="product-card-link"><div className="product-image"><ProductImage product={product} loading="lazy" />{!product.stock && <span className="stock-badge">Out of stock</span>}<span className="product-arrow" aria-hidden="true">↗</span></div><div className="product-meta"><span>{product.brand}</span><span className="product-rating" aria-label={`Rated ${product.rating} out of 5`}>★ {(product.rating == null ? 'Unrated' : product.rating.toFixed(1))}</span></div><div className="product-title"><h3>{product.name}</h3><span>${product.price.toFixed(2)}</span></div><p className="product-caption">{product.type} · {product.color}</p></Link></article>;
}
