import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Browse products with optional filters
export const getProducts = async (filters = {}) => {
  try {
    const params = new URLSearchParams();

    if (filters.type) params.append('type', filters.type);
    if (filters.color) params.append('color', filters.color);
    if (filters.size) params.append('size', filters.size);
    if (filters.price_min) params.append('price_min', filters.price_min);
    if (filters.price_max) params.append('price_max', filters.price_max);

    const response = await api.get(`/api/products?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

// Get single product by ID
export const getProductById = async (id) => {
  try {
    const response = await api.get(`/api/products/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
    throw error;
  }
};

// Get featured products
export const getFeaturedProducts = async () => {
  try {
    const response = await api.get('/api/featured');
    return response.data;
  } catch (error) {
    console.error('Error fetching featured products:', error);
    throw error;
  }
};

// Natural language AI search
export const searchProducts = async (query) => {
  try {
    const response = await api.post('/api/search', { query });
    return response.data;
  } catch (error) {
    console.error('Error searching products:', error);
    throw error;
  }
};

// Get categories
export const getCategories = async () => {
  try {
    const response = await api.get('/api/categories');
    return response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
    throw error;
  }
};

export default api;
