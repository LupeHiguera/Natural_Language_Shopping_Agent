import { useState } from 'react';
import { Link } from 'react-router-dom';
import AISearchBar from './AISearchBar';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        {/* Top section with logo and nav */}
        <div className="flex items-center justify-between py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-blue-600">
              ShoeHub
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium transition">
              Home
            </Link>
            <Link to="/browse?type=mens" className="text-gray-700 hover:text-blue-600 font-medium transition">
              Men's
            </Link>
            <Link to="/browse?type=womens" className="text-gray-700 hover:text-blue-600 font-medium transition">
              Women's
            </Link>
            <Link to="/browse?sale=true" className="text-gray-700 hover:text-blue-600 font-medium transition">
              Sale
            </Link>
            <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium transition">
              About
            </Link>
          </nav>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-md hover:bg-gray-100"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {mobileMenuOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* AI Search Bar */}
        <div className="pb-4">
          <AISearchBar />
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden pb-4 border-t pt-4">
            <nav className="flex flex-col space-y-2">
              <Link
                to="/"
                className="text-gray-700 hover:text-blue-600 font-medium py-2 px-4 rounded hover:bg-gray-50 transition"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/browse?type=mens"
                className="text-gray-700 hover:text-blue-600 font-medium py-2 px-4 rounded hover:bg-gray-50 transition"
                onClick={() => setMobileMenuOpen(false)}
              >
                Men's
              </Link>
              <Link
                to="/browse?type=womens"
                className="text-gray-700 hover:text-blue-600 font-medium py-2 px-4 rounded hover:bg-gray-50 transition"
                onClick={() => setMobileMenuOpen(false)}
              >
                Women's
              </Link>
              <Link
                to="/browse?sale=true"
                className="text-gray-700 hover:text-blue-600 font-medium py-2 px-4 rounded hover:bg-gray-50 transition"
                onClick={() => setMobileMenuOpen(false)}
              >
                Sale
              </Link>
              <Link
                to="/about"
                className="text-gray-700 hover:text-blue-600 font-medium py-2 px-4 rounded hover:bg-gray-50 transition"
                onClick={() => setMobileMenuOpen(false)}
              >
                About
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;