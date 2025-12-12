import { Link } from 'react-router-dom';
import { useState } from 'react';

const ProductCard = ({ product }) => {
  const [imageError, setImageError] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  const fallbackImage = `https://via.placeholder.com/400x300/4F46E5/FFFFFF?text=${encodeURIComponent(product.name)}`;

  return (
    <div className="group bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden">
      <Link to={`/product/${product.shoe_id}`} className="block">
        {/* Image Section */}
        <div className="relative overflow-hidden bg-gray-100 aspect-[4/3]">
          <img
            src={imageError ? fallbackImage : product.image_url}
            alt={product.name}
            onError={() => setImageError(true)}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
          />

          {/* Favorite Button */}
          <button
            onClick={(e) => {
              e.preventDefault();
              setIsFavorite(!isFavorite);
            }}
            className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-md hover:bg-gray-50 transition"
          >
            <svg
              className={`w-5 h-5 ${isFavorite ? 'fill-red-500 text-red-500' : 'fill-none text-gray-400'}`}
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </button>

          {/* Stock Badge */}
          {!product.in_stock && (
            <div className="absolute top-3 left-3 px-3 py-1 bg-red-500 text-white text-xs font-semibold rounded-full">
              Out of Stock
            </div>
          )}
        </div>

        {/* Product Info */}
        <div className="p-4">
          <div className="mb-2">
            <p className="text-xs text-gray-500 uppercase tracking-wide">{product.brand}</p>
            <h3 className="font-semibold text-gray-800 line-clamp-2 group-hover:text-blue-600 transition">
              {product.name}
            </h3>
          </div>

          <div className="flex items-center justify-between mb-2">
            <span className="text-xl font-bold text-gray-900">
              ${product.price.toFixed(2)}
            </span>
            {product.rating && (
              <div className="flex items-center">
                <svg className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                  <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                </svg>
                <span className="ml-1 text-sm text-gray-600">{product.rating.toFixed(1)}</span>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600 capitalize">{product.type}</span>
            <span className="text-gray-600">
              {product.sizes && product.sizes.length > 0 && (
                `Sizes: ${Math.min(...product.sizes)}-${Math.max(...product.sizes)}`
              )}
            </span>
          </div>

          {product.color && (
            <div className="mt-2 flex items-center">
              <span className="text-xs text-gray-500 mr-2">Color:</span>
              <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded capitalize">
                {product.color}
              </span>
            </div>
          )}
        </div>
      </Link>

      {/* Quick View Button */}
      <div className="px-4 pb-4">
        <Link
          to={`/product/${product.shoe_id}`}
          className="block w-full text-center py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition font-medium"
        >
          View Details
        </Link>
      </div>
    </div>
  );
};

export default ProductCard;