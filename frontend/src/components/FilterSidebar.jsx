import { useState } from 'react';

const FilterSidebar = ({ onFilterChange, currentFilters }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState(currentFilters || {});

  const shoeTypes = ['running', 'casual', 'formal', 'athletic', 'boots', 'sandals', 'sneakers'];
  const colors = ['black', 'white', 'red', 'blue', 'brown', 'gray', 'green', 'pink', 'yellow'];
  const sizes = [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13];
  const priceRanges = [
    { label: 'Under $50', min: 0, max: 50 },
    { label: '$50 - $100', min: 50, max: 100 },
    { label: '$100 - $150', min: 100, max: 150 },
    { label: '$150 - $200', min: 150, max: 200 },
    { label: '$200+', min: 200, max: 999 },
  ];

  const handleFilterChange = (filterType, value) => {
    const newFilters = { ...filters, [filterType]: value };
    if (!value || value === '') {
      delete newFilters[filterType];
    }
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const handlePriceRange = (min, max) => {
    const newFilters = { ...filters, price_min: min, price_max: max };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    setFilters({});
    onFilterChange({});
  };

  const FilterContent = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-gray-800">Filters</h3>
        <button
          onClick={clearFilters}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          Clear All
        </button>
      </div>

      {/* Shoe Type Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Shoe Type
        </label>
        <select
          value={filters.type || ''}
          onChange={(e) => handleFilterChange('type', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Types</option>
          {shoeTypes.map((type) => (
            <option key={type} value={type} className="capitalize">
              {type}
            </option>
          ))}
        </select>
      </div>

      {/* Color Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Color
        </label>
        <div className="grid grid-cols-3 gap-2">
          {colors.map((color) => (
            <button
              key={color}
              onClick={() => handleFilterChange('color', filters.color === color ? '' : color)}
              className={`px-3 py-2 rounded-md text-sm font-medium capitalize transition ${
                filters.color === color
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {color}
            </button>
          ))}
        </div>
      </div>

      {/* Size Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Size
        </label>
        <select
          value={filters.size || ''}
          onChange={(e) => handleFilterChange('size', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Sizes</option>
          {sizes.map((size) => (
            <option key={size} value={size}>
              {size}
            </option>
          ))}
        </select>
      </div>

      {/* Price Range Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Price Range
        </label>
        <div className="space-y-2">
          {priceRanges.map((range) => (
            <button
              key={range.label}
              onClick={() => handlePriceRange(range.min, range.max)}
              className={`w-full px-3 py-2 rounded-md text-sm font-medium text-left transition ${
                filters.price_min === range.min && filters.price_max === range.max
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {range.label}
            </button>
          ))}
        </div>
      </div>

      {/* Custom Price Range */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Custom Price Range
        </label>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            placeholder="Min"
            value={filters.price_min || ''}
            onChange={(e) => handleFilterChange('price_min', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span className="text-gray-500">-</span>
          <input
            type="number"
            placeholder="Max"
            value={filters.price_max || ''}
            onChange={(e) => handleFilterChange('price_max', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile Filter Toggle */}
      <div className="lg:hidden mb-4">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          <span className="font-medium text-gray-700">Filters</span>
          <svg
            className={`w-5 h-5 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        {isOpen && (
          <div className="mt-4 p-4 bg-white border border-gray-200 rounded-md">
            <FilterContent />
          </div>
        )}
      </div>

      {/* Desktop Sidebar */}
      <div className="hidden lg:block bg-white p-6 rounded-lg shadow-md">
        <FilterContent />
      </div>
    </>
  );
};

export default FilterSidebar;