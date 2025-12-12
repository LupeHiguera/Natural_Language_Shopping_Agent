import { useState } from 'react';

const ProductDetail = ({ product }) => {
  const [selectedSize, setSelectedSize] = useState(null);
  const [imageError, setImageError] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  if (!product) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-center">
          <p className="text-gray-600">Product not found</p>
        </div>
      </div>
    );
  }

  const fallbackImage = `https://via.placeholder.com/600x450/4F46E5/FFFFFF?text=${encodeURIComponent(product.name)}`;

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
        {/* Image Section */}
        <div className="relative">
          <img
            src={imageError ? fallbackImage : product.image_url}
            alt={product.name}
            onError={() => setImageError(true)}
            className="w-full h-auto rounded-lg"
          />
          <button
            onClick={() => setIsFavorite(!isFavorite)}
            className="absolute top-4 right-4 p-3 bg-white rounded-full shadow-lg hover:bg-gray-50 transition"
          >
            <svg
              className={`w-6 h-6 ${isFavorite ? 'fill-red-500 text-red-500' : 'fill-none text-gray-400'}`}
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
        </div>

        {/* Product Info Section */}
        <div>
          <div className="mb-6">
            <p className="text-sm text-gray-500 uppercase tracking-wide mb-2">{product.brand}</p>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>

            {product.rating && (
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      className={`w-5 h-5 ${i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'} fill-current`}
                      viewBox="0 0 20 20"
                    >
                      <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z" />
                    </svg>
                  ))}
                  <span className="ml-2 text-sm text-gray-600">{product.rating.toFixed(1)} / 5.0</span>
                </div>
              </div>
            )}

            <div className="text-4xl font-bold text-gray-900 mb-4">
              ${product.price.toFixed(2)}
            </div>
          </div>

          {/* Product Details */}
          <div className="mb-6 space-y-3">
            <div className="flex items-center">
              <span className="text-gray-600 w-24">Type:</span>
              <span className="font-medium text-gray-900 capitalize">{product.type}</span>
            </div>
            <div className="flex items-center">
              <span className="text-gray-600 w-24">Color:</span>
              <span className="font-medium text-gray-900 capitalize">{product.color}</span>
            </div>
            <div className="flex items-center">
              <span className="text-gray-600 w-24">Stock:</span>
              <span className={`font-medium ${product.in_stock ? 'text-green-600' : 'text-red-600'}`}>
                {product.in_stock ? 'In Stock' : 'Out of Stock'}
              </span>
            </div>
          </div>

          {/* Size Selection */}
          {product.sizes && product.sizes.length > 0 && (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Select Size
              </label>
              <div className="grid grid-cols-5 gap-2">
                {product.sizes.map((size) => (
                  <button
                    key={size}
                    onClick={() => setSelectedSize(size)}
                    className={`py-2 px-4 border rounded-md font-medium transition ${
                      selectedSize === size
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-blue-600'
                    }`}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Description */}
          {product.description && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
              <p className="text-gray-600 leading-relaxed">{product.description}</p>
            </div>
          )}

          {/* Add to Cart Button */}
          <div className="space-y-3">
            <button
              disabled={!product.in_stock}
              className="w-full py-3 px-6 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
            >
              {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
            </button>
            <button className="w-full py-3 px-6 bg-gray-100 text-gray-800 rounded-lg font-semibold hover:bg-gray-200 transition">
              Add to Wishlist
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;