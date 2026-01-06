# AWS Bedrock Shopping Agent - Weekend Learning Plan

## Goal
Demonstrate AWS + Terraform competency for Deckers Brands GenAI Lead role. You already have the app—now you need the infrastructure skills.

## Time Budget: 16 hours + evenings

---

## Pre-Work (Friday Evening - 1 hour)

- [ ] AWS account created with billing alerts ($20 budget)
- [ ] AWS CLI installed and configured (`aws configure`)
- [ ] Terraform installed (`terraform -v`)
- [ ] VS Code AWS Toolkit extension installed
- [ ] Bookmark: [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [ ] Bookmark: [Bedrock Agents Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [ ] Enable Bedrock model access in AWS console (Claude 3 Haiku) - this can take a few minutes

---

## Day 1: Infrastructure with Terraform (Saturday - 8 hours)

### Block 1: Terraform Foundations (2 hours)
**Objective**: Provision DynamoDB table with Terraform

- [ ] Create `infrastructure/` directory in project
- [ ] Create `main.tf` with AWS provider
- [ ] Create `dynamodb.tf` - define ShoeInventory table
- [ ] Run `terraform init`
- [ ] Run `terraform plan` - review what will be created
- [ ] Run `terraform apply` - create the table
- [ ] Verify table exists in AWS console

**Checkpoint**: You can explain what Terraform state is and why it matters.

### Block 2: Lambda with Terraform (2.5 hours)
**Objective**: Deploy Lambda function via Terraform

- [ ] Create `lambda/search_shoes/lambda_function.py`
- [ ] Create `iam.tf` - Lambda execution role + DynamoDB read policy
- [ ] Create `lambda.tf` - Lambda function resource
- [ ] Create `outputs.tf` - Export Lambda ARN
- [ ] Package Lambda code (zip file)
- [ ] `terraform apply` - deploy Lambda
- [ ] Test Lambda in AWS console with test event

**Checkpoint**: Lambda successfully queries DynamoDB and returns results.

### Block 3: Seed Data (1 hour)
**Objective**: Populate DynamoDB with test products

- [ ] Create `data/seed_data.json` (50 shoes)
- [ ] Create `data/populate_db.py` script
- [ ] Run script to populate table
- [ ] Verify data in DynamoDB console
- [ ] Test Lambda again with real data

**Checkpoint**: Lambda returns actual shoe data based on filters.

### Block 4: API Gateway with Terraform (1.5 hours)
**Objective**: Expose Lambda via REST API

- [ ] Create `api_gateway.tf`
- [ ] Define REST API, resource, method, integration
- [ ] Enable CORS
- [ ] Create deployment stage (`prod`)
- [ ] `terraform apply`
- [ ] Test endpoint with curl

**Checkpoint**: `curl https://[api-id].execute-api.[region].amazonaws.com/prod/search` returns data.

### Block 5: Documentation (1 hour)
**Objective**: Document what you learned

- [ ] Create architecture diagram (draw.io or excalidraw)
- [ ] Document each Terraform file's purpose
- [ ] Note any issues you hit and how you solved them
- [ ] Commit everything to git

**End of Day 1 Deliverable**: Full infrastructure provisioned via Terraform, Lambda querying DynamoDB, API Gateway exposing endpoint.

---

## Day 2: Bedrock Agent + Integration (Sunday - 8 hours)

### Block 1: Bedrock Agent Setup (2 hours)
**Objective**: Create working Bedrock Agent

- [ ] Navigate to Bedrock console → Agents
- [ ] Create agent: `ShoeShoppingAgent`
- [ ] Select Claude 3 Haiku model
- [ ] Write initial agent instructions (see claude.md)
- [ ] Create IAM role for agent (Bedrock needs Lambda invoke permission)
- [ ] Prepare agent (creates first version)
- [ ] Test in Bedrock console with simple query

**Checkpoint**: Agent responds to "What shoes do you have?"

### Block 2: Action Group Configuration (2 hours)
**Objective**: Connect agent to your Lambda

- [ ] Create OpenAPI schema for action group (`bedrock/action_schema.json`)
- [ ] Add action group to agent
- [ ] Point to your Lambda function
- [ ] Update Lambda to handle Bedrock agent event format
- [ ] Prepare agent again
- [ ] Test: "Show me running shoes under $100"

**Checkpoint**: Agent invokes Lambda and returns real product data.

### Block 3: Prompt Engineering (2 hours)
**Objective**: Make the agent actually good

This is where your Wells Fargo experience transfers. Iterate on instructions.

- [ ] Test 10 different queries, document results
- [ ] Identify failure patterns (ambiguous queries, wrong parameters)
- [ ] Refine instructions to handle edge cases
- [ ] Test again, measure improvement
- [ ] Document your prompt iterations in `docs/prompt_engineering.md`

**Test queries to try**:
```
"red running shoes"
"something comfortable under $80"
"size 10"
"I need shoes for a wedding"
"what's your cheapest option"
"Nike shoes"
"show me everything"
```

**Checkpoint**: Agent handles 8/10 test queries correctly.

### Block 4: Connect to Your Backend (1.5 hours)
**Objective**: Integrate Bedrock with existing FastAPI app

- [ ] Add Bedrock agent invocation to `backend/app/bedrock_client.py`
- [ ] Update `/api/search` endpoint to call agent
- [ ] Test from your local backend
- [ ] Verify frontend search bar works end-to-end

**Checkpoint**: Type in frontend search bar → get real results from Bedrock agent.

### Block 5: Deploy Frontend (0.5 hours)
**Objective**: Host frontend on S3

- [ ] Add `s3.tf` for static website bucket
- [ ] `npm run build` your frontend
- [ ] `terraform apply` to create bucket
- [ ] Upload build files to S3
- [ ] Test public URL

**Checkpoint**: Live URL showing your app.

---

## Evenings: Polish

### Monday Evening (1-2 hours)
- [ ] Clean up Terraform files (add comments, organize)
- [ ] Write README.md with setup instructions
- [ ] Create GitHub repo, push code
- [ ] Add demo link and screenshot to README

### Tuesday Evening (1-2 hours)
- [ ] Update resume with project
- [ ] Practice explaining the architecture
- [ ] Prepare for "walk me through how this works" question
- [ ] Send resume to friend for referral

---

## Interview Talking Points

After completing this, you can speak to:

1. **Terraform/IaC**: "I provisioned DynamoDB, Lambda, API Gateway, S3, and IAM roles all through Terraform. I understand state management, resource dependencies, and the apply workflow."

2. **Bedrock Agents**: "I built an agent with custom action groups. The agent parses natural language queries and invokes a Lambda function to search the product database. I iterated on the prompts to handle ambiguous queries."

3. **Serverless Architecture**: "The architecture is fully serverless—API Gateway triggers Lambda, Lambda queries DynamoDB. No servers to manage, scales automatically."

4. **Transferable Skills**: "This is similar to what I do at Wells Fargo with Semantic Kernel and Gemini, just on AWS instead of Azure. The prompt engineering patterns are the same."

5. **Learning Speed**: "I built this in a weekend to ramp up on AWS. I can learn new platforms quickly because I understand the underlying concepts."

---

## If You Get Stuck

**Terraform errors**: Usually IAM permissions. Check the error message, it usually tells you what permission is missing.

**Lambda not working**: Check CloudWatch logs. Add print statements and redeploy.

**Bedrock agent not invoking Lambda**: Check IAM role attached to agent has `lambda:InvokeFunction` permission.

**CORS errors**: Make sure API Gateway has CORS enabled AND your Lambda returns CORS headers.

---

## Success Criteria

By end of weekend:
- [ ] All infrastructure defined in Terraform (can `terraform destroy` and `terraform apply` to recreate)
- [ ] Bedrock agent answers product queries correctly
- [ ] Frontend deployed and accessible via public URL
- [ ] Can explain every component and why it exists
- [ ] GitHub repo with clean code and documentation