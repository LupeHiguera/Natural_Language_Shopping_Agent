import { useState, useEffect, useCallback } from 'react';
import { getProducts, getFeaturedProducts, getErrorMessage } from '../services/api';

const useCatalog = (filterKey, featured) => {
  const [state, setState] = useState({ key: null, products: [], loading: true, error: null });
  const [attempt, setAttempt] = useState(0);
  const key = `${featured}:${filterKey}:${attempt}`;
  useEffect(() => {
    const controller = new AbortController();
    const fetchProducts = async () => {
      setState({ key, products: [], loading: true, error: null });
      try {
        const options = { signal: controller.signal };
        const products = featured ? await getFeaturedProducts(options) : await getProducts(JSON.parse(filterKey), options);
        if (!controller.signal.aborted) setState({ key, products, loading: false, error: null });
      } catch (error) {
        if (!controller.signal.aborted) setState({ key, products: [], loading: false, error: getErrorMessage(error) });
      }
    };
    fetchProducts();
    return () => controller.abort();
  }, [filterKey, featured, key]);
  const retry = useCallback(() => setAttempt(value => value + 1), []);
  return { ...(state.key === key ? state : { products: [], loading: true, error: null }), retry };
};
export const useProducts = (filters = {}) => useCatalog(JSON.stringify(filters), false);
export const useFeaturedProducts = () => useCatalog('{}', true);
