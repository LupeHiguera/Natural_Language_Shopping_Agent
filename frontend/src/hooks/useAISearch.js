import { useState, useRef, useEffect, useCallback } from 'react';
import { searchProducts, getErrorMessage } from '../services/api';

export const useAISearch = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const controller = useRef(null);
  const session = useRef(null);
  const requestId = useRef(0);
  useEffect(() => () => controller.current?.abort(), []);
  const clearResults = useCallback(() => {
    requestId.current += 1;
    controller.current?.abort();
    session.current = null;
    setResults(null);
    setError(null);
    setLoading(false);
  }, []);
  const search = async (value) => {
    const query = value.trim();
    if (!query) return clearResults();
    controller.current?.abort();
    const current = ++requestId.current;
    const request = new AbortController();
    controller.current = request;
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const data = await searchProducts(query, session.current, { signal: request.signal });
      if (requestId.current !== current || request.signal.aborted) return;
      session.current = data.session_id;
      setResults({ ...data, query });
    } catch (err) {
      if (requestId.current === current && !request.signal.aborted) setError(getErrorMessage(err));
    } finally {
      if (requestId.current === current && !request.signal.aborted) setLoading(false);
    }
  };
  return { results, loading, error, search, clearResults };
};
