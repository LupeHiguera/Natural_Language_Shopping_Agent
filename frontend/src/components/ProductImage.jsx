import { useState } from 'react';
export default function ProductImage({ product, className = '', ...props }) {
  const [failed, setFailed] = useState(false);
  return failed || !product.image_url ? <div className={`image-placeholder ${className}`} role="img" aria-label={`${product.name}, image unavailable`}><span aria-hidden="true">↗</span><span>{product.brand}</span><small>Image unavailable</small></div> : <img src={product.image_url} alt={`${product.name} in ${product.color}`} onError={() => setFailed(true)} className={className} {...props} />;
}
