import { useState } from 'react';
import { Link } from 'react-router-dom';
import AISearchBar from './AISearchBar';

const links = [['/browse', 'All shoes'], ['/browse?type=running', 'Running'], ['/browse?type=casual', 'Everyday'], ['/browse?type=formal', 'Formal'], ['/about', 'The project']];
export default function Header() {
  const [open, setOpen] = useState(false);
  return <header className="site-header">
    <div className="shell header-row">
      <Link to="/" className="brand" aria-label="ShoeHub home"><span className="brand-mark" aria-hidden="true">s.</span>ShoeHub</Link>
      <nav className="desktop-nav" aria-label="Main navigation">{links.map(([to, label]) => <Link key={to} to={to} className="nav-link">{label}</Link>)}</nav>
      <span className="demo-tag">A shopping experiment</span>
      <button className="menu-button" aria-label={open ? 'Close navigation' : 'Open navigation'} aria-expanded={open} aria-controls="mobile-nav" onClick={() => setOpen(!open)}>{open ? '✕' : '☰'}</button>
    </div>
    {open && <nav id="mobile-nav" className="mobile-nav shell" aria-label="Mobile navigation">{links.map(([to, label]) => <Link key={to} to={to} onClick={() => setOpen(false)}>{label}</Link>)}</nav>}
    <div className="shell header-search"><AISearchBar /></div>
  </header>;
}
