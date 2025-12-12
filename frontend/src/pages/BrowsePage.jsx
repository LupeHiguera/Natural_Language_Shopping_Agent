import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import ProductGrid from '../components/ProductGrid';
import FilterSidebar from '../components/FilterSidebar';
import { useProducts } from '../hooks/useProducts';

const BrowsePage = () => {
  const [searchParams] = useSearchParams();
  const [filters, setFilters] = useState({});

  // Initialize filters from URL params
  useEffect(() => {
    const params = {};
    if (searchParams.get('type')) params.type = searchParams.get('type');
    if (searchParams.get('color')) params.color = searchParams.get('color');
    if (searchParams.get('size')) params.size = searchParams.get('size');
    if (searchParams.get('price_min')) params.price_min = searchParams.get('price_min');
    if (searchParams.get('price_max')) params.price_max = searchParams.get('price_max');
    setFilters(params);
  }, [searchParams]);

  const { products, loading, error } = useProducts(filters);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Browse Shoes</h1>
          <p className="text-gray-600">
            {products?.length > 0
              ? `Showing ${products.length} ${products.length === 1 ? 'product' : 'products'}`
              : 'Explore our collection'}
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Filter Sidebar */}
          <div className="lg:col-span-1">
            <FilterSidebar
              onFilterChange={handleFilterChange}
              currentFilters={filters}
            />
          </div>

          {/* Product Grid */}
          <div className="lg:col-span-3">
            <ProductGrid products={products} loading={loading} error={error} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrowsePage;