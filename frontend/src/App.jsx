import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import BrowsePage from './pages/BrowsePage';
import ProductPage from './pages/ProductPage';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/browse" element={<BrowsePage />} />
            <Route path="/product/:id" element={<ProductPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

// Simple About Page Component
const AboutPage = () => {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">About ShoeHub</h1>
        <div className="prose prose-lg">
          <p className="text-gray-600 mb-4">
            Welcome to ShoeHub, your premier destination for premium footwear shopping powered by AI technology.
          </p>
          <p className="text-gray-600 mb-4">
            This is a learning project built to explore AWS Bedrock Agents, prompt engineering, and modern web development practices.
            The application demonstrates how AI can enhance the shopping experience through natural language search capabilities.
          </p>
          <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">Technology Stack</h2>
          <ul className="list-disc pl-6 text-gray-600 space-y-2">
            <li>Frontend: React 18+ with Vite and Tailwind CSS</li>
            <li>Backend: FastAPI (Python)</li>
            <li>AI: AWS Bedrock with Claude 3.5 Haiku</li>
            <li>Database: Amazon DynamoDB</li>
            <li>Infrastructure: AWS Lambda, API Gateway, S3, CloudFront</li>
          </ul>
          <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">Features</h2>
          <ul className="list-disc pl-6 text-gray-600 space-y-2">
            <li>AI-powered natural language product search</li>
            <li>Traditional browsing with filters (type, color, size, price)</li>
            <li>Responsive design for all devices</li>
            <li>Fast and efficient product discovery</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default App;