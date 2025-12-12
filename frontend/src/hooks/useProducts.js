import { useState, useEffect } from 'react';
import { getProducts, getFeaturedProducts } from '../services/api';

export const useProducts = (filters = {}) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getProducts(filters);
        setProducts(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [JSON.stringify(filters)]);

  return { products, loading, error };
};

export const useFeaturedProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFeatured = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getFeaturedProducts();
        setProducts(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch featured products');
      } finally {
        setLoading(false);
      }
    };

    fetchFeatured();
  }, []);

  return { products, loading, error };
};