import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import BrowsePage from './pages/BrowsePage';
import ProductPage from './pages/ProductPage';
function AboutPage() {
  return <div className="shell section-space about-page"><p className="eyebrow">Behind the experiment</p><h1 className="page-title">A more natural way<br />to find your next pair.</h1><p>ShoeHub is a portfolio project exploring product discovery through natural language. Describe a style, color, size, or budget, or use the collection filters to find your fit.</p><p>The project pairs a React interface with a FastAPI backend, Amazon DynamoDB, and AWS Bedrock Agents. Local development includes a sample catalog and a simple keyword search so the browsing experience can be explored without AWS.</p><div className="demo-notice"><strong>Built for exploration.</strong><p>This is a demonstration, with sample product data and illustrative photography. Checkout, payment, and shipping are not available.</p></div><Link to="/browse" className="button button-dark">Explore the collection ↗</Link></div>;
}
function NotFoundPage() {
  return <div className="shell section-space catalog-state"><p className="eyebrow">404 / A wrong turn</p><h1 className="page-title">Let’s get you back on track.</h1><Link className="button button-dark" to="/">Back to ShoeHub ↗</Link></div>;
}
export default function App() {
  return <Router><div className="app"><a className="skip-link" href="#main-content">Skip to content</a><Header /><main id="main-content" tabIndex={-1}><Routes><Route path="/" element={<HomePage />} /><Route path="/browse" element={<BrowsePage />} /><Route path="/product/:id" element={<ProductPage />} /><Route path="/about" element={<AboutPage />} /><Route path="*" element={<NotFoundPage />} /></Routes></main><Footer /></div></Router>;
}
