# AWS Bedrock Shopping Agent - Learning Project

## Project Overview
A shoe shopping website hosted on AWS featuring a Bedrock Agent that enables natural language search through a product database. This project focuses on learning AWS services, Bedrock Agent configuration, and prompt engineering while using AI-assisted coding for the application layer.

## Primary Learning Objectives
1. **AWS Service Configuration & Deployment** - Hands-on experience with AWS console and infrastructure setup
2. **Bedrock Agent Development** - Building and configuring agents with action groups
3. **Prompt Engineering** - Crafting effective prompts for natural language product search
4. **AWS Integration Patterns** - Connecting frontend → API Gateway → Bedrock → Lambda → DynamoDB

## Tech Stack (DO NOT DEVIATE)

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Deployment**: AWS S3 + CloudFront

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AWS SDK**: boto3
- **Bedrock Runtime**: boto3 bedrock-agent-runtime client
- **Lambda Runtime**: Python 3.11
- **API**: AWS API Gateway (REST API)

### Database
- **Primary Database**: Amazon DynamoDB
- **Table Name**: `ShoeInventory`
- **Partition Key**: `shoe_id` (String)

### AWS Services (Core Focus)
- Amazon Bedrock (Bedrock Agents)
- AWS Lambda (Action Groups)
- Amazon DynamoDB (Product Database)
- Amazon S3 (Static Website Hosting)
- Amazon API Gateway (REST API)
- AWS IAM (Roles & Permissions)
- Amazon CloudFront (Optional CDN)
- AWS CloudWatch (Logging & Monitoring)

### Bedrock Configuration
- **Foundation Model**: Anthropic Claude 3.5 Haiku (cost-efficient for learning)
- **Agent Type**: Bedrock Agent with Action Groups
- **Action Groups**: Custom Lambda functions for shoe search

## Project Structure
```
aws-bedrock-shopping-agent/
├── frontend/                    # React application (VIBE CODE)
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx              # Main navigation + AI search bar
│   │   │   ├── AISearchBar.jsx         # Natural language search input
│   │   │   ├── SearchResults.jsx       # Agent response + products panel
│   │   │   ├── ProductGrid.jsx         # Browseable grid of shoes
│   │   │   ├── ProductCard.jsx         # Individual shoe card
│   │   │   ├── FilterSidebar.jsx       # Category/price/size filters
│   │   │   ├── Hero.jsx                # Homepage hero section
│   │   │   ├── Footer.jsx              # Site footer
│   │   │   └── ProductDetail.jsx       # Single product view
│   │   ├── pages/
│   │   │   ├── HomePage.jsx            # Landing page
│   │   │   ├── BrowsePage.jsx          # Browse all products
│   │   │   └── ProductPage.jsx         # Product detail page
│   │   ├── services/
│   │   │   └── api.js                  # API Gateway calls
│   │   ├── hooks/
│   │   │   ├── useProducts.js          # Product data management
│   │   │   └── useAISearch.js          # AI search functionality
│   │   ├── App.jsx                     # Main app with routing
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # FastAPI application (VIBE CODE)
│   ├── app/
│   │   ├── main.py                     # FastAPI app with all endpoints
│   │   ├── bedrock_client.py           # Bedrock agent invocation
│   │   ├── dynamodb_client.py          # Direct DynamoDB queries
│   │   ├── models.py                   # Pydantic models
│   │   └── config.py                   # Configuration
│   ├── requirements.txt
│   └── Dockerfile (optional)
│
├── lambda/                      # AWS Lambda functions (FOCUS AREA)
│   ├── search_shoes/
│   │   ├── lambda_function.py  # Main handler for agent actions
│   │   ├── requirements.txt
│   │   └── README.md           # Lambda-specific setup
│   └── layer/                   # Shared dependencies
│
├── bedrock/                     # Bedrock Agent configuration (FOCUS AREA)
│   ├── agent_instructions.txt  # Main agent prompt
│   ├── action_group_schema.json # OpenAPI schema for actions
│   └── setup_guide.md          # Step-by-step AWS console instructions
│
├── infrastructure/              # AWS setup documentation (FOCUS AREA)
│   ├── dynamodb_setup.md       # DynamoDB table creation
│   ├── iam_policies.json       # Required IAM policies
│   ├── api_gateway_setup.md    # API Gateway configuration
│   └── s3_cloudfront_setup.md  # Frontend hosting setup
│
├── data/
│   ├── seed_data.json          # Sample shoe inventory (100-150 shoes)
│   └── populate_db.py          # Script to populate DynamoDB
│
├── docs/
│   ├── aws_setup_checklist.md  # Complete AWS setup steps
│   ├── bedrock_agent_guide.md  # Detailed agent configuration
│   └── prompt_engineering.md   # Prompt iteration notes
│
├── .env.example
├── .gitignore
└── README.md
```

## Phase 1: Quick App Foundation (VIBE CODE - 4-6 hours)

### Frontend (React + Vite + Tailwind)
**Ask Claude Code to create:**
```
A full-featured shoe shopping website with AI-powered search:

LAYOUT:
- Header with logo, navigation menu, and AI search bar (replaces traditional search)
- Navigation: Home, Men's, Women's, Sale, About
- Hero section on homepage with featured collections
- Product grid showing all/filtered shoes
- Footer with links and information

AI SEARCH BAR (Primary Feature):
- Prominent search bar in header (always visible)
- Placeholder: "Try: 'red running shoes under $100 in size 10'"
- Natural language input processing
- Floating results panel when search is active
- Shows both agent response text AND matching products
- Can dismiss to return to browsing

BROWSING FEATURES:
- Category filters (type, color, price range, size)
- Sort options (price, newest, popular)
- Product grid with cards showing: image, name, brand, price, colors available
- Click product card for detail view
- Pagination or infinite scroll

PRODUCT CARDS:
- High-quality placeholder images
- Hover effects
- Quick view option
- Add to favorites (UI only for learning project)

STATE MANAGEMENT:
- Browse mode: Shows all/filtered products from initial load
- Search mode: Shows agent results when search is used
- Seamless transition between browsing and searching

RESPONSIVE DESIGN:
- Mobile-first approach
- Hamburger menu for mobile
- Collapsible filters
- Tailwind CSS utility classes
```

**Key Files to Generate:**
- `Header.jsx` - Navigation and AI search bar component
- `AISearchBar.jsx` - Natural language search input with results panel
- `SearchResults.jsx` - Agent response and product results display
- `ProductGrid.jsx` - Browseable product grid component
- `ProductCard.jsx` - Individual shoe display card
- `FilterSidebar.jsx` - Traditional category/price filters
- `HomePage.jsx` - Landing page with hero and featured products
- `ProductDetailView.jsx` - Individual product detail page
- `api.js` - API Gateway integration for both search and browse
- `App.jsx` - Main application with routing
- `hooks/useProducts.js` - Custom hook for product data management

### Backend (FastAPI)
**Ask Claude Code to create:**
```
A FastAPI application with multiple endpoints:

ENDPOINTS:
- GET /api/products - Retrieve all products with optional filters (type, color, price_min, price_max, size)
- GET /api/products/{shoe_id} - Get single product details
- POST /api/search - Natural language search via Bedrock agent
- GET /api/featured - Get featured products for homepage
- GET /api/categories - Get all available categories/types

CORE FUNCTIONALITY:
- Boto3 integration with bedrock-agent-runtime for AI search
- Direct DynamoDB queries for browsing/filtering (no agent needed)
- Function to invoke Bedrock agent with user natural language query
- Response parsing to extract both agent text response AND shoe results
- Caching layer for frequently browsed categories (optional)
- CORS middleware for local development
- Environment variable configuration for AWS credentials
- Pydantic models for request/response validation
- Proper error handling and HTTP status codes

SEARCH FLOW:
User query → Bedrock agent → Agent uses Lambda action → Lambda queries DynamoDB → Results return

BROWSE FLOW:
User filters → FastAPI → Direct DynamoDB query → Results return
```

**Key Files to Generate:**
- `main.py` - FastAPI app with all endpoints
- `bedrock_client.py` - Bedrock agent invocation logic (search only)
- `dynamodb_client.py` - Direct DynamoDB operations (browsing)
- `models.py` - All Pydantic models:
  - `SearchRequest`, `SearchResponse` (agent search)
  - `ProductFilter`, `ProductListResponse` (browsing)
  - `ShoeProduct`, `ProductDetail` (product data)
- `config.py` - Environment and AWS configuration

### Mock Data
**Ask Claude Code to create:**
```
A JSON file with 100-150 sample shoes for a realistic browsing experience:
- shoe_id (unique UUID format)
- name (e.g., "Air Max 270", "Classic Leather Loafer")
- brand (Nike, Adidas, Puma, Reebok, New Balance, Clarks, etc.)
- type (running, casual, formal, athletic, boots, sandals, sneakers)
- color (primary color - red, blue, black, white, brown, gray, etc.)
- sizes (array of available sizes: [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13])
- price (range $30-$300, varied distribution)
- image_url (use placeholder image URLs from unsplash or placeholder.com)
- description (2-3 sentences about the shoe)
- featured (boolean - mark 8-10 shoes as featured for homepage)
- rating (4.0-5.0 for UI purposes)
- stock (in_stock boolean)

Ensure good variety:
- 30% running/athletic
- 25% casual/sneakers
- 20% formal
- 15% boots
- 10% sandals
- Mix of colors across all types
- Range of price points in each category
```

**Vibe Coding Prompt Examples:**

**For Full Shopping Site:**
```
"Create a React e-commerce site for shoes with:
- Header containing logo, nav menu (Home, Men's, Women's, Sale), and AI-powered 
  search bar with placeholder 'Try: red running shoes under $100'
- Homepage with hero section and product grid
- Product cards showing image, name, brand, price
- FilterSidebar component with category, color, price, and size filters
- AISearchBar component that sends natural language to API and shows results 
  in a floating panel with both agent response text and matching products
- Product detail view page
- Responsive design with Tailwind CSS
- React Router for navigation
- Axios for API calls"
```

**For Backend with Dual Functionality:**
```
"Create a FastAPI app with these endpoints:
1. GET /api/products - Returns all products, supports query params for filtering 
   (type, color, size, price_min, price_max), directly queries DynamoDB
2. POST /api/search - Accepts natural language query, invokes AWS Bedrock agent 
   using boto3 bedrock-agent-runtime, returns both agent text response and 
   matching shoe products
3. GET /api/products/{shoe_id} - Returns single product details
4. GET /api/featured - Returns featured products

Include CORS, environment variables for AWS credentials and Bedrock agent ID, 
Pydantic models for all requests/responses, and proper error handling. Create 
separate client modules for Bedrock and DynamoDB operations."
```

## Phase 2: AWS Infrastructure Setup (FOCUS AREA - 6-8 hours)

### Step 2.1: DynamoDB Table Creation
**Manual AWS Console Steps:**
1. Navigate to DynamoDB console
2. Create table: `ShoeInventory`
3. Partition key: `shoe_id` (String)
4. Use on-demand billing mode (cost-efficient for learning)
5. Enable point-in-time recovery (optional)
6. Create Global Secondary Indexes (GSI):
   - `type-index` (Partition key: `type`)
   - `color-index` (Partition key: `color`)
   - `price-index` (Partition key: `price_range`, create attribute)

**Populate Database:**
- Run `data/populate_db.py` script to load seed data
- Verify data in DynamoDB console

### Step 2.2: Lambda Function Setup
**Manual AWS Console Steps:**
1. Create Lambda function: `SearchShoesFunction`
2. Runtime: Python 3.11
3. Architecture: x86_64
4. Create execution role with policies:
   - `AWSLambdaBasicExecutionRole`
   - Custom DynamoDB read policy (provide JSON)
5. Upload lambda code from `lambda/search_shoes/`
6. Add boto3 layer if needed
7. Set timeout to 30 seconds
8. Configure environment variables if needed

**Lambda Function Logic (You Code This):**
```python
# lambda/search_shoes/lambda_function.py
# This function receives structured parameters from Bedrock agent
# and queries DynamoDB for matching shoes

def lambda_handler(event, context):
    # Extract parameters: type, color, size, min_price, max_price
    # Query DynamoDB with filters
    # Return formatted results to agent
    pass
```

### Step 2.3: IAM Role Configuration
**Manual AWS Console Steps:**
1. Create role: `BedrockAgentRole`
2. Trust policy: Allow Bedrock service
3. Attach policies:
   - Allow InvokeModel on Claude models
   - Allow Lambda:InvokeFunction on SearchShoesFunction
4. Create role: `APIGatewayBedrockRole`
5. Attach policies:
   - Allow bedrock:InvokeAgent

**Document all ARNs** for later use

### Step 2.4: API Gateway Setup
**Manual AWS Console Steps:**
1. Create REST API: `ShoeShoppingAPI`
2. Create resources and methods:
   - `/products` - GET (browse all/filtered products)
   - `/products/{shoe_id}` - GET (single product)
   - `/search` - POST (AI natural language search)
   - `/featured` - GET (featured products)
3. Integration type options:
   - **Option A (Simpler)**: Lambda proxy integration to FastAPI
   - **Option B (More AWS-native)**: Direct integration with Bedrock + Lambda
4. Enable CORS on all endpoints
5. Create deployment stage: `prod`
6. Note the invoke URL

**Recommended Approach for Learning:**
Use Option A (Lambda proxy to FastAPI) - simpler and lets you iterate faster on the backend logic while focusing on Bedrock/prompt engineering.

**Alternative Architecture:**
- `/products` endpoints → Direct Lambda → DynamoDB (fast browsing)
- `/search` endpoint → Lambda → Bedrock Agent → Search Lambda → DynamoDB

## Phase 3: Bedrock Agent Configuration (PRIMARY FOCUS - 8-12 hours)

### Step 3.1: Create Bedrock Agent
**Manual AWS Console Steps:**
1. Navigate to Amazon Bedrock console
2. Go to "Agents" section
3. Click "Create Agent"
4. Agent name: `ShoeShoppingAgent`
5. Select model: Anthropic Claude 3.5 Haiku
6. Agent resource role: Use created `BedrockAgentRole`

### Step 3.2: Write Agent Instructions (PROMPT ENGINEERING FOCUS)
**This is where you learn prompt engineering:**

```
bedrock/agent_instructions.txt:

You are a helpful shopping assistant for a shoe store. Your role is to 
help customers find shoes based on their preferences using natural language.

You can search for shoes based on:
- Type: running, casual, formal, athletic, boots, sandals, sneakers
- Color: any color (red, blue, black, white, etc.)
- Size: US sizes 6-13
- Price range: $30-$300

When a customer asks for shoes, you should:
1. Extract the relevant criteria from their request
2. Use the search_shoes action to query the database
3. Present the results in a friendly, conversational way
4. If multiple shoes match, highlight the top 5-10 results
5. Include relevant details: name, price, available sizes, color

Examples of queries you should handle:
- "Show me red running shoes under $100"
- "I need size 10 casual shoes"
- "What black formal shoes do you have?"
- "Looking for comfortable athletic shoes around $80"

Always be helpful and ask clarifying questions if the request is unclear.
```

**Iteration Focus:**
- Test different instruction phrasings
- Adjust tone and detail level
- Handle edge cases (no results, ambiguous queries)
- Document what works and what doesn't

### Step 3.3: Create Action Group
**Manual AWS Console Steps:**
1. In agent configuration, add "Action Group"
2. Name: `SearchShoesAction`
3. Action group type: Define with API schemas
4. Lambda function: Select `SearchShoesFunction`
5. Upload OpenAPI schema (see below)

**OpenAPI Schema (bedrock/action_group_schema.json):**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Shoe Search API",
    "version": "1.0.0",
    "description": "API for searching shoe inventory"
  },
  "paths": {
    "/searchShoes": {
      "post": {
        "summary": "Search for shoes based on criteria",
        "description": "Searches the shoe inventory based on type, color, size, and price range",
        "operationId": "searchShoes",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "type": {
                    "type": "string",
                    "description": "Type of shoe (running, casual, formal, athletic, boots)",
                    "enum": ["running", "casual", "formal", "athletic", "boots", "sandals", "sneakers"]
                  },
                  "color": {
                    "type": "string",
                    "description": "Shoe color"
                  },
                  "size": {
                    "type": "number",
                    "description": "US shoe size (6-13)"
                  },
                  "min_price": {
                    "type": "number",
                    "description": "Minimum price in USD"
                  },
                  "max_price": {
                    "type": "number",
                    "description": "Maximum price in USD"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful search",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "shoes": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "shoe_id": {"type": "string"},
                          "name": {"type": "string"},
                          "brand": {"type": "string"},
                          "type": {"type": "string"},
                          "color": {"type": "string"},
                          "sizes": {"type": "array", "items": {"type": "number"}},
                          "price": {"type": "number"},
                          "image_url": {"type": "string"}
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Step 3.4: Prepare and Test Agent
**Manual AWS Console Steps:**
1. Click "Prepare" to create agent version
2. Wait for preparation to complete
3. Use built-in test interface
4. Create alias: `prod-v1`

**Test Queries:**

**Natural Language Search (Through AI Bar):**
```
- "Show me running shoes"
- "I need size 10 casual shoes under $100"
- "What red shoes do you have?"
- "Looking for formal shoes between $80 and $150"
- "Show me all athletic shoes"
- "I want black sneakers for everyday wear"
- "Comfortable walking shoes around $75"
- "Do you have any boots under $120?"
- "Show me shoes similar to Nike Air Max"
- "What's on sale right now?"
```

**Ambiguous/Edge Case Queries:**
```
- "Show me shoes" (should ask for preferences)
- "Cheap shoes" (should clarify price range)
- "Something for running" (should confirm running shoes)
- "Red" (should ask what type of red shoe)
- "Size 10" (should ask what style/type)
```

**Browse Flow Testing:**
```
- Filter by: Running shoes
- Filter by: Price $50-$100
- Filter by: Color = Black
- Filter by: Size = 10
- Combine: Running + Red + Size 10 + Under $100
- Sort by: Price (low to high)
- Sort by: Newest
```

**Document:**
- Which queries work well
- Which queries confuse the agent
- How to improve instructions
- Parameter extraction accuracy

## Phase 4: Frontend Deployment (FOCUS AREA - 2-3 hours)

### Step 4.1: Build React App
```bash
cd frontend
npm run build
```

### Step 4.2: S3 Setup
**Manual AWS Console Steps:**
1. Create S3 bucket: `shoe-shopping-app-[unique-id]`
2. Disable "Block all public access"
3. Enable static website hosting
4. Index document: `index.html`
5. Error document: `index.html`
6. Upload `dist/` contents
7. Add bucket policy for public read:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::shoe-shopping-app-[unique-id]/*"
  }]
}
```

### Step 4.3: CloudFront Setup (Optional)
**Manual AWS Console Steps:**
1. Create CloudFront distribution
2. Origin: S3 bucket website endpoint
3. Viewer protocol: Redirect HTTP to HTTPS
4. Price class: Use North America and Europe only (cost savings)
5. Default root object: `index.html`
6. Custom error responses: 404 → /index.html (for React routing)

## Phase 5: Integration & Testing (2-4 hours)

### Integration Steps

**Browse Flow Integration:**
1. User lands on homepage → sees featured products
2. User clicks category or applies filter → frontend calls `/api/products` with params
3. FastAPI queries DynamoDB directly
4. Products display in grid
5. User clicks product → detail view from `/api/products/{id}`

**AI Search Flow Integration:**
1. User types natural language in search bar: "red running shoes under $100 size 10"
2. Frontend calls `/api/search` POST endpoint
3. FastAPI invokes Bedrock agent
4. Agent interprets query and calls Lambda action
5. Lambda queries DynamoDB with extracted parameters
6. Agent formats response with natural language + product list
7. Search results panel shows both agent text and products
8. User can dismiss to return to browsing

**End-to-End Test Flow:**
```
Homepage → Browse Products → Apply Filter → View Product Details
           ↓
      Use AI Search Bar → See Agent Response + Results → Click Product
```

### Testing Checklist

**Browse Functionality:**
- [ ] Homepage loads featured products
- [ ] Category filters work (type, color, price, size)
- [ ] Product grid displays correctly
- [ ] Product cards show all information
- [ ] Product detail view loads
- [ ] Pagination/infinite scroll works
- [ ] Responsive on mobile

**AI Search Functionality:**
- [ ] Search bar accepts natural language input
- [ ] Agent correctly interprets queries
- [ ] Agent extracts parameters (type, color, size, price)
- [ ] Lambda filters DynamoDB correctly
- [ ] Results include both agent text AND products
- [ ] Search results panel displays properly
- [ ] Can return to browsing after search
- [ ] Loading states work during search

**Performance & UX:**
- [ ] Browse results load in <1 second
- [ ] AI search completes in <3 seconds
- [ ] Smooth transitions between modes
- [ ] No layout shift during loading
- [ ] Error handling works gracefully
- [ ] Mobile responsive design
- [ ] Search bar always accessible

**Agent Quality:**
- [ ] Handles ambiguous queries ("show me shoes")
- [ ] Asks clarifying questions when needed
- [ ] Understands price phrases ("under $100", "around $80")
- [ ] Recognizes shoe types from descriptions
- [ ] Provides helpful response even with no results
- [ ] Natural, conversational tone

## Key Learning Areas (FOCUS HERE)

### 1. Prompt Engineering
**What to Learn:**
- How instruction clarity affects agent behavior
- Parameter extraction accuracy
- Handling ambiguous queries
- Conversational tone vs. robotic responses
- Few-shot examples vs. general instructions

**Experiments to Try:**
- Different instruction lengths (brief vs. detailed)
- Various example formats
- Constraint enforcement (price limits, size validation)
- Error message tone and helpfulness

### 2. Action Group Design
**What to Learn:**
- OpenAPI schema structure for Bedrock
- Parameter definition best practices
- How schema affects agent's understanding
- Required vs. optional parameters
- Enum constraints for categorical data

### 3. Lambda Integration
**What to Learn:**
- Event structure from Bedrock agent
- Response format requirements
- Error handling and propagation
- Timeout considerations
- Cold start optimization

### 4. DynamoDB Query Patterns
**What to Learn:**
- Efficient querying with GSIs
- Filter expressions
- Scan vs. Query performance
- Cost optimization for learning projects

### 5. AWS IAM & Security
**What to Learn:**
- Principle of least privilege
- Service-to-service authentication
- Trust relationships
- Policy debugging

## Environment Variables

### Frontend (.env)
```
VITE_API_GATEWAY_URL=https://[api-id].execute-api.[region].amazonaws.com/prod
```

### Backend (.env)
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=[your-key]
AWS_SECRET_ACCESS_KEY=[your-secret]
BEDROCK_AGENT_ID=[agent-id]
BEDROCK_AGENT_ALIAS_ID=[alias-id]
```

### Lambda (Environment Variables in AWS Console)
```
DYNAMODB_TABLE_NAME=ShoeInventory
AWS_REGION=us-east-1
```

## Development Workflow

### Local Development

**Phase 1: Build with Mock Data**
1. Run React dev server: `cd frontend && npm run dev`
2. Run FastAPI locally: `cd backend && uvicorn app.main:app --reload`
3. Start with fully mocked responses:
   - `/api/products` returns static JSON from local file
   - `/api/search` returns mock agent responses
4. Build and style the full UI without AWS dependencies

**Phase 2: Add DynamoDB Integration**
1. Populate DynamoDB with seed data
2. Connect `/api/products` endpoints to real DynamoDB
3. Test browse functionality end-to-end
4. Keep `/api/search` mocked initially

**Phase 3: Add Bedrock Agent**
1. Configure Bedrock agent in AWS console
2. Connect `/api/search` to real Bedrock agent
3. Test natural language queries
4. Iterate on agent prompts

### Local Testing Strategies

**Browse Testing:**
- Test category filters with mock data
- Verify pagination logic
- Check responsive design at various breakpoints
- Test product detail view navigation

**Search Testing:**
- Initially mock agent responses to build UI
- Switch to real agent once AWS is configured
- Keep sample queries in a test file for regression testing
- Monitor agent response quality and iterate on prompts

### AWS Testing

**Bedrock Agent:**
1. Use Bedrock agent test console for rapid prompt iteration
2. Test queries without involving frontend
3. Document which instructions work best
4. Create a "test query suite" to run after each prompt change

**Lambda Functions:**
1. Test Lambda independently via AWS console test feature
2. Monitor CloudWatch logs for errors
3. Verify DynamoDB queries return expected results
4. Check execution time and memory usage

**API Gateway:**
1. Use API Gateway test feature for each endpoint
2. Verify request/response transformations
3. Test CORS headers
4. Check authorization (if implemented)

**End-to-End:**
1. Test from deployed frontend to production AWS
2. Monitor all AWS services in real-time
3. Check CloudWatch logs across all services
4. Verify cost tracking in AWS Cost Explorer

### Deployment

**Frontend Deployment:**
1. Build production bundle: `npm run build`
2. Upload to S3: `aws s3 sync dist/ s3://[bucket-name]/ --delete`
3. Invalidate CloudFront cache: `aws cloudfront create-invalidation --distribution-id [ID] --paths "/*"`
4. Test production site

**Backend Deployment:**
1. Package Lambda functions with dependencies
2. Upload to AWS Lambda via console or CLI
3. Update environment variables if changed
4. Test via API Gateway

**Agent Updates:**
1. Modify agent instructions in console
2. Click "Prepare" to create new version
3. Update alias to point to new version
4. Test with production frontend

### Iteration Cycle

**For Browsing Features:**
- Update component → Hot reload → Test → Commit
- Backend changes → Restart server → Test → Commit

**For AI Search:**
1. Identify issue with agent response
2. Update agent instructions in AWS console
3. Prepare new agent version
4. Test in agent console
5. Test from frontend
6. Document changes in `docs/prompt_engineering.md`
7. Repeat

**Prompt Engineering Workflow:**
```
Test Query → Poor Result → Analyze Why → Update Instructions → 
Re-prepare Agent → Test Again → Document → Next Query
```

Track metrics:
- Query understanding accuracy
- Parameter extraction success rate
- Response relevance
- Response time
- User satisfaction (qualitative)

## Cost Monitoring

### Set Up Billing Alerts
1. AWS Budgets: Create $20/month budget
2. Email alerts at 50%, 80%, 100%
3. Monitor daily with Cost Explorer

### Expected Costs Breakdown
- Bedrock (Haiku): $2-5/month (main cost)
- Lambda: $0 (free tier)
- DynamoDB: $0 (free tier for low volume)
- S3: $0-1/month
- API Gateway: $0 (free tier)
- CloudFront: $0 (free tier first year)

**Total: $2-10/month for learning usage**

## Success Metrics

### AWS Learning Goals
- [ ] Configured 5+ AWS services independently
- [ ] Created IAM roles with proper permissions
- [ ] Deployed serverless architecture
- [ ] Set up API Gateway integration
- [ ] Monitored with CloudWatch

### Bedrock Agent Goals
- [ ] Created functional agent with action groups
- [ ] Iterated on prompts 10+ times
- [ ] Agent handles 80%+ of test queries correctly
- [ ] Response time under 3 seconds
- [ ] Natural conversational responses

### Integration Goals
- [ ] End-to-end request flow works
- [ ] Proper error handling at each layer
- [ ] Responsive UI with good UX
- [ ] Deployed to production AWS environment

## Next Steps After Completion

### Enhancements to Try
1. Add more action groups (check inventory, get recommendations)
2. Implement conversation memory in Bedrock agent
3. Add user authentication with Cognito
4. Create admin panel for inventory management
5. Add analytics tracking
6. Implement caching layer
7. Use Step Functions for complex workflows

### Advanced AWS Learning
- CloudFormation/CDK for infrastructure as code
- CI/CD with CodePipeline
- Monitoring dashboards with CloudWatch
- Cost optimization with Reserved Instances
- Multi-region deployment

## Troubleshooting Guide

### Common Issues

**Agent not invoking Lambda:**
- Check IAM role permissions
- Verify Lambda ARN in action group
- Check Lambda execution role has DynamoDB access

**No results from queries:**
- Verify DynamoDB has data
- Check Lambda CloudWatch logs
- Test Lambda function independently
- Verify GSI configuration

**CORS errors:**
- Add proper CORS headers in API Gateway
- Configure CORS in FastAPI
- Check CloudFront CORS if using CDN

**High Bedrock costs:**
- Use Haiku instead of Sonnet
- Optimize prompt length
- Add query caching
- Limit testing frequency

## Resources

### AWS Documentation
- [Amazon Bedrock Agents Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [Lambda Python Runtime](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [API Gateway REST API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)

### Learning Resources
- AWS Bedrock Prompt Engineering best practices
- DynamoDB query optimization patterns
- IAM policy debugging techniques

## Notes for Claude Code

When working with Claude Code on this project:

**For Frontend (Vibe Code):**
- "Create a React shoe e-commerce site with Tailwind CSS, header with navigation and AI search bar, product grid for browsing, and filter sidebar"
- "Build an AISearchBar component that sends natural language queries to API and displays results in a floating panel with both agent text and product cards"
- "Create a ProductGrid component with ProductCard children that displays shoe inventory"
- "Build a HomePage with hero section and featured products grid"
- "Add React Router with routes for home, browse, and product detail pages"
- "Set up Axios to call these API endpoints: GET /api/products, POST /api/search, GET /api/products/{id}, GET /api/featured"

**For Backend (Vibe Code):**
- "Create FastAPI app with GET /api/products endpoint that accepts query params (type, color, size, price_min, price_max) and queries DynamoDB directly using boto3"
- "Add POST /api/search endpoint that invokes Bedrock agent and returns both agent response text and matching products"
- "Create GET /api/products/{shoe_id} endpoint for single product details"
- "Write bedrock_client.py with agent invocation using boto3 bedrock-agent-runtime"
- "Write dynamodb_client.py with functions to query products with filters"
- "Add Pydantic models for ProductFilter, SearchRequest, SearchResponse, ShoeProduct"
- "Include CORS middleware and environment variable configuration"

**For Lambda (You Code, Claude Code assists):**
- "Help me structure a Lambda function that receives parameters from Bedrock agent (type, color, size, price range) and queries DynamoDB with those filters"
- "Debug this Lambda error: [paste error]"
- "Optimize this DynamoDB query for performance"
- "Add error handling for when no products match the criteria"

**For Data (Vibe Code):**
- "Generate 100 sample shoes in JSON format with attributes: shoe_id, name, brand, type, color, sizes array, price, image_url, description, featured boolean, rating, stock status. Include variety across types and price ranges."
- "Write Python script to populate DynamoDB table 'ShoeInventory' from JSON file using boto3"

**For Styling (Vibe Code):**
- "Style the header with a modern e-commerce design, prominent search bar, and mobile-responsive hamburger menu"
- "Create hover effects for product cards with smooth transitions"
- "Design the search results floating panel with backdrop blur and slide-down animation"
- "Make the filter sidebar collapsible on mobile with Tailwind"

**Important Distinctions for Claude Code:**
- The AI search bar is PART OF the site, not the whole site
- Users can browse products traditionally OR use natural language search
- The search bar should be prominent but not the only navigation method
- Both flows (browse and search) need to work independently and smoothly
- Mock both flows initially, then connect to real AWS services

## Project Timeline

- **Week 1**: Vibe code app, AWS account setup
- **Week 2**: DynamoDB, Lambda, IAM configuration (DEEP FOCUS)
- **Week 3**: Bedrock agent creation and prompt engineering (DEEP FOCUS)
- **Week 4**: Integration, testing, deployment
- **Ongoing**: Prompt iteration and optimization

---

## Quick Start Commands

```bash
# Clone and setup
git clone [your-repo-url]
cd aws-bedrock-shopping-agent

# Frontend setup
cd frontend
npm install
npm run dev
# Access at http://localhost:5173

# Backend setup (in new terminal)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# API at http://localhost:8000

# Populate DynamoDB (after AWS setup)
cd data
python populate_db.py

# Build frontend for deployment
cd frontend
npm run build

# Deploy frontend to S3
aws s3 sync dist/ s3://shoe-shopping-app-[unique-id]/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id [ID] --paths "/*"

# View Lambda logs
aws logs tail /aws/lambda/SearchShoesFunction --follow

# Test API endpoints locally
curl http://localhost:8000/api/products
curl http://localhost:8000/api/products?type=running&price_max=100
curl -X POST http://localhost:8000/api/search -H "Content-Type: application/json" -d '{"query": "red running shoes under $100"}'
```

**Development Flow:**
```bash
# Terminal 1: Frontend dev server
cd frontend && npm run dev

# Terminal 2: Backend dev server  
cd backend && uvicorn app.main:app --reload

# Terminal 3: Watch Lambda logs (once deployed)
aws logs tail /aws/lambda/SearchShoesFunction --follow
```

---

**Remember**: The goal is AWS and Bedrock learning. Vibe code the app quickly, then spend 70% of your time on AWS configuration, agent development, and prompt engineering. Document everything you learn!

**Key Success Factors:**
1. ✅ Build a functional shopping site where users can browse OR search
2. ✅ AI search bar seamlessly integrates into normal shopping flow
3. ✅ Agent correctly interprets natural language and returns relevant products
4. ✅ All AWS services properly configured and communicating
5. ✅ Documented prompt engineering learnings for future reference
6. 