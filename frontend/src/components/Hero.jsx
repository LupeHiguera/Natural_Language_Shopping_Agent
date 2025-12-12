import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 text-white overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-20"></div>

      <div className="relative container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-3xl">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            Find Your Perfect Shoes with AI
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-blue-100">
            Shop smarter with our AI-powered search. Just describe what you're looking for in natural language.
          </p>

          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              to="/browse"
              className="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition text-center"
            >
              Browse All Shoes
            </Link>
            <button
              onClick={() => {
                const searchInput = document.querySelector('input[type="text"]');
                if (searchInput) {
                  searchInput.focus();
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }
              }}
              className="px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition text-center"
            >
              Try AI Search
            </button>
          </div>
        </div>
      </div>

      {/* Decorative Elements */}
      <div className="absolute top-0 right-0 -mt-12 -mr-12 w-64 h-64 bg-blue-400 rounded-full opacity-20 blur-3xl"></div>
      <div className="absolute bottom-0 left-0 -mb-12 -ml-12 w-64 h-64 bg-purple-400 rounded-full opacity-20 blur-3xl"></div>
    </div>
  );
};

export default Hero;