import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ProductDetail from '../components/ProductDetail';
import { getProductById, getErrorMessage } from '../services/api';
export default function ProductPage() {
  const { id } = useParams();
  const [state, setState] = useState({ id: null, product: null, error: null });
  useEffect(() => {
    const request = new AbortController();
    const load = async () => {
      try {
        const product = await getProductById(id, { signal: request.signal });
        if (!request.signal.aborted) setState({ id, product, error: null });
      } catch (error) {
        if (!request.signal.aborted) setState({ id, product: null, error: error.response?.status === 404 ? 'This pair could not be found.' : getErrorMessage(error) });
      }
    };
    load();
    return () => request.abort();
  }, [id]);
  return <div className="shell section-space"><nav className="breadcrumbs" aria-label="Breadcrumb"><Link to="/">Home</Link><span aria-hidden="true">/</span><Link to="/browse">Collection</Link><span aria-hidden="true">/</span><span>{state.id === id ? state.product?.name || 'Product' : 'Product'}</span></nav>{state.id !== id ? <div className="catalog-state" role="status"><span className="spinner" />Loading your pair…</div> : state.error ? <div className="catalog-state" role="alert"><h1>Let’s find another pair.</h1><p>{state.error}</p><Link to="/browse" className="button button-dark">Back to the collection ↗</Link></div> : <ProductDetail key={id} product={state.product} />}</div>;
}
