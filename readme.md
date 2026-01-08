# AWS Bedrock GenAI Shopping Agent

A natural language shoe shopping application powered by AWS Bedrock Agents. Users can search for products using conversational queries like "show me red running shoes under $100" and the AI agent interprets the request, queries the database, and returns matching products.

![Architecture Diagram](docs/architecture.png)

## 🎯 Live Demo

**[Try it here →](https://your-cloudfront-url.com)**

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   React     │────▶│   FastAPI   │────▶│  AWS Bedrock    │
│  Frontend   │     │   Backend   │     │     Agent       │
└─────────────┘     └─────────────┘     └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │  Lambda Action  │
                                        │     Group       │
                                        └────────┬────────┘
                                                 │
                                                 ▼
                                        ┌─────────────────┐
                                        │    DynamoDB     │
                                        │  ShoeInventory  │
                                        └─────────────────┘
```

**Request Flow:**
1. User enters natural language query (e.g., "comfortable running shoes under $80")
2. FastAPI backend invokes Bedrock Agent
3. Agent parses query and extracts parameters (type: running, max_price: 80)
4. Agent calls Lambda action group with structured parameters
5. Lambda queries DynamoDB with filters
6. Results flow back through agent with conversational response
7. Frontend displays products with agent's response

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, Tailwind CSS, Axios |
| Backend | FastAPI, Python 3.11, boto3 |
| AI/ML | AWS Bedrock Agent, Claude 4.5 Haiku |
| Database | Amazon DynamoDB |
| Infrastructure | Terraform, AWS Lambda, API Gateway |
| Deployment | S3, CloudFront |

## 📁 Project Structure

```
├── frontend/                # React application
│   ├── src/
│   │   ├── components/      # UI components (SearchBar, ProductCard, etc.)
│   │   ├── hooks/           # Custom hooks (useAISearch, useProducts)
│   │   └── services/        # API client
│   └── package.json
│
├── backend/                 # FastAPI application
│   └── app/
│       ├── main.py          # API endpoints
│       ├── bedrock_client.py # Bedrock Agent invocation
│       └── models.py        # Pydantic models
│
├── lambda/                  # AWS Lambda functions
│   └── search_shoes/
│       └── lambda_function.py
│
├── infra/                   # Terraform infrastructure
│   ├── main.tf              # AWS provider config
│   ├── dynamodb.tf          # DynamoDB table
│   ├── lambda.tf            # Lambda function
│   ├── iam.tf               # IAM roles & policies
│   └── apigateway.tf        # API Gateway
│
└── data/
    ├── seed_data.json       # Sample shoe inventory
    └── populate_db.py       # Database seeder
```

## 🚀 AWS Services Used

- **Amazon Bedrock** - LLM orchestration with Agents and Action Groups
- **AWS Lambda** - Serverless compute for database queries
- **Amazon DynamoDB** - NoSQL database for product inventory
- **Amazon API Gateway** - REST API endpoint
- **Amazon S3** - Static website hosting
- **Amazon CloudFront** - CDN for frontend delivery
- **AWS IAM** - Roles and policies for service permissions

## 🔧 Infrastructure as Code

All AWS infrastructure is provisioned using Terraform:

```bash
cd infra
terraform init
terraform plan
terraform apply
```

Key resources:
- DynamoDB table with on-demand billing
- Lambda function with DynamoDB read permissions
- IAM roles for Lambda execution and Bedrock Agent
- API Gateway with CORS configuration

## 💡 Key Learnings

### Bedrock Agent Architecture
- Agents use **Action Groups** to define available tools
- Each action group maps to a Lambda function
- OpenAPI schema defines parameters the agent can extract
- Agent decides when to invoke actions based on user query

### Lambda Event Formats
The Lambda handles two different event formats:
- **API Gateway**: `{ "body": "{\"query\": \"...\"}" }`
- **Bedrock Agent**: `{ "actionGroup": "...", "parameters": [...] }`

### DynamoDB + Python
- boto3 returns `Decimal` types, not native Python floats
- Requires custom JSON encoder for serialization:
```python
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super().default(o)
```

### Prompt Engineering
Iterated on agent instructions to:
- Search immediately without asking clarifying questions
- Extract partial parameters (search with what's provided)
- Return structured product data alongside conversational response

## 🏃 Running Locally

### Prerequisites
- Node.js 18+
- Python 3.11+
- AWS CLI configured
- Terraform installed

### Frontend
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# http://localhost:8000
```

### Environment Variables

**Backend (.env):**
```
AWS_REGION=us-east-1
BEDROCK_AGENT_ID=your-agent-id
BEDROCK_AGENT_ALIAS_ID=your-alias-id
```

## 📊 Sample Queries

The agent handles natural language queries like:

| Query | Extracted Parameters |
|-------|---------------------|
| "red running shoes under $100" | type: running, color: red, max_price: 100 |
| "size 10 casual shoes" | type: casual, size: 10 |
| "comfortable boots around $150" | type: boots, min_price: 130, max_price: 170 |
| "show me all athletic shoes" | type: athletic |

## 🔒 Security Considerations

- CORS restricted to specific origins (no wildcard)
- IAM roles follow least-privilege principle
- No credentials committed to repository
- API Gateway with request validation

## 📈 Future Enhancements

- [ ] Add CloudWatch dashboard for observability
- [ ] Implement CI/CD with GitHub Actions
- [ ] Add user authentication with Cognito
- [ ] Conversation memory for multi-turn queries
- [ ] Product recommendations based on browsing history

## 👤 Author

**Guadalupe Higuera**
- GitHub: [https://github.com/LupeHiguera](https://github.com/yourusername)
- LinkedIn: [https://www.linkedin.com/in/guadalupe-higuera/](https://linkedin.com/in/yourprofile)
- Email: Guadalupe.Higuera@protonmail.com

## 📄 License

MIT License - feel free to use this project for learning purposes.