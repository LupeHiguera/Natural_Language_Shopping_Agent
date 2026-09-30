import { Link } from 'react-router-dom';
export default function Footer() {
  return <footer className="site-footer"><div className="shell"><div className="footer-top"><div><Link to="/" className="brand">ShoeHub</Link><p>A better way to find your next pair.</p></div><nav aria-label="Footer navigation"><Link to="/browse">The collection ↗</Link><Link to="/about">About the project ↗</Link></nav></div><div className="footer-bottom"><span>© {new Date().getFullYear()} ShoeHub</span><span>A portfolio shopping demo · No purchases or payments</span></div></div></footer>;
}
