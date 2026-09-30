import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_GATEWAY_URL || 'http://localhost:8000',
  timeout: 30000,
});

export const getProducts = async (filters = {}, options = {}) => {
  const params = Object.fromEntries(Object.entries(filters).filter(([, value]) => value !== '' && value != null));
  const { data } = await api.get('/api/products', { params, ...options });
  return data.products || [];
};
export const getProductById = async (id, options = {}) => {
  const { data } = await api.get(`/api/products/${encodeURIComponent(id)}`, options);
  return data;
};
export const getFeaturedProducts = async (options = {}) => {
  const { data } = await api.get('/api/featured', options);
  return data.products || [];
};
export const searchProducts = async (query, sessionId, options = {}) => {
  const { data } = await api.post('/api/search', { query, session_id: sessionId }, options);
  return data;
};
export const getCategories = async (options = {}) => {
  const { data } = await api.get('/api/categories', options);
  return data;
};
export const getErrorMessage = (error) => {
  if (error.code === 'ECONNABORTED') return 'This is taking longer than expected. Please try again.';
  if (!error.response) return 'The catalog is unavailable right now. Please try again shortly.';
  const detail = error.response.data?.detail;
  if (error.response.status < 500 && typeof detail === 'string') return detail;
  if (error.response.status === 422) return 'Please check your search or filter values and try again.';
  return 'Something went wrong. Please try again.';
};
export default api;
