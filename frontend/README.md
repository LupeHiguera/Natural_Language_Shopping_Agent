# ShoeHub Frontend

React frontend for the AWS Bedrock Shopping Agent learning project.

## Tech Stack

- **React 18+** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls

## Project Structure

```
src/
├── components/         # Reusable UI components
│   ├── Header.jsx      # Main navigation + AI search bar
│   ├── AISearchBar.jsx # Natural language search input
│   ├── SearchResults.jsx # Agent response + products panel
│   ├── ProductGrid.jsx  # Grid of product cards
│   ├── ProductCard.jsx  # Individual shoe display card
│   ├── FilterSidebar.jsx # Category/price/size filters
│   ├── Hero.jsx         # Homepage hero section
│   ├── Footer.jsx       # Site footer
│   └── ProductDetail.jsx # Single product view
├── pages/              # Page components
│   ├── HomePage.jsx    # Landing page
│   ├── BrowsePage.jsx  # Browse all products
│   └── ProductPage.jsx # Product detail page
├── services/           # API integration
│   └── api.js          # API Gateway calls
├── hooks/              # Custom React hooks
│   ├── useProducts.js  # Product data management
│   └── useAISearch.js  # AI search functionality
├── App.jsx             # Main app with routing
└── main.jsx            # Entry point
```

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend running on `http://localhost:8000` (or update `.env`)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Update .env with your API endpoint (defaults to localhost:8000)
```

### Development

```bash
# Start dev server
npm run dev

# Access at http://localhost:5173
```

### Build for Production

```bash
# Create production build
npm run build

# Preview production build locally
npm run preview
```

## Features

### AI Search
- Natural language search bar in header
- Example: "red running shoes under $100 in size 10"
- Displays agent response and matching products
- Floating results panel with dismiss option

### Browse Mode
- Traditional product browsing
- Filter by type, color, size, price
- Responsive product grid
- Click cards for detail view

### Product Pages
- Detailed product information
- Size selection
- Image gallery
- Add to cart/wishlist (UI only)

## Environment Variables

Create a `.env` file:

```env
# Local development
VITE_API_GATEWAY_URL=http://localhost:8000

# Production
# VITE_API_GATEWAY_URL=https://[api-id].execute-api.[region].amazonaws.com/prod
```

## API Endpoints Used

- `GET /api/products` - Browse with filters
- `GET /api/products/{id}` - Single product
- `GET /api/featured` - Featured products
- `POST /api/search` - AI natural language search

## Deployment to AWS S3

```bash
# Build production bundle
npm run build

# Upload to S3 (replace with your bucket name)
aws s3 sync dist/ s3://shoe-shopping-app-[unique-id]/ --delete

# Invalidate CloudFront cache (if using CDN)
aws cloudfront create-invalidation --distribution-id [ID] --paths "/*"
```

## Development Notes

- The app works with or without a backend (will show errors gracefully)
- All API calls include error handling
- Loading states are shown during data fetches
- Responsive design works on mobile, tablet, and desktop
- Images fallback to placeholders if URLs fail

## Learn More

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)