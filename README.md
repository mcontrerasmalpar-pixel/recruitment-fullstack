# Recruitment Management System - Fullstack Application

Complete serverless recruitment management system with Angular frontend and Python Lambda backend.

## 📋 Project Structure

```
recruitment-fullstack/
├── src/                          # Angular frontend source code
│   ├── app/                      # Application components
│   ├── assets/                   # Static assets
│   ├── environments/             # Environment configurations
│   │   ├── environment.ts        # Development environment
│   │   └── environment.prod.ts   # Production environment
│   └── main.ts                   # Application entry point
├── public/                       # Public assets
├── backend/                      # Python Lambda backend
│   ├── infrastructure/           # SAM CloudFormation templates
│   │   └── template.yaml        # SAM infrastructure template
│   ├── sql/                      # Database schemas and migrations
│   ├── lambda_function.py        # Lambda handler code
│   └── requirements.txt          # Python dependencies
├── angular.json                  # Angular build configuration
├── package.json                  # Frontend dependencies
├── tsconfig.json                 # TypeScript configuration
└── amplify.yml                   # Amplify deployment configuration
```

## 🚀 Deployment via AWS Amplify

### Prerequisites

- AWS Account with appropriate permissions
- GitHub repository access (for source control)
- Node.js 18+ installed locally

### Step 1: Push Code to GitHub

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial fullstack application setup"

# Add remote (replace with your GitHub repository)
git remote add origin https://github.com/mcontrerasmalpar-pixel/recruitment-fullstack.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy via Amplify Console

1. **Log in to AWS Console**: https://console.aws.amazon.com
2. **Navigate to Amplify**: Search for "Amplify" and open Amplify Console
3. **Create New App**:
   - Click "Create App"
   - Select "Host Web App"
   - Choose "GitHub" as source control provider
   - Authorize and select your repository
   - Select "main" branch
   - Review build settings (use defaults from amplify.yml)
   - Deploy

### Step 3: Configure Environment Variables

In Amplify Console:

1. **Frontend Environment**:
   - Go to App Settings > Environment Variables
   - Add: `API_URL` = Your API Gateway endpoint

2. **Backend Environment Variables** (if deploying backend via Amplify):
   - Add database credentials:
     - `DB_HOST`: Your RDS endpoint
     - `DB_NAME`: callcenter
     - `DB_USER`: Your database username
     - `DB_PASSWORD`: Your database password
     - `VPC_ID`: Your VPC ID
     - `PRIVATE_SUBNET_1`: Subnet ID
     - `PRIVATE_SUBNET_2`: Subnet ID
     - `LAMBDA_SECURITY_GROUP`: Security group ID
     - `CORS_ORIGIN`: Your frontend domain
     - `ALERT_EMAIL`: Your email

### Step 4: Backend Deployment (Manual or via Amplify)

**Option A: Deploy Backend Separately (Recommended)**

```bash
cd backend/infrastructure
aws configure  # Set up AWS credentials
sam build
sam deploy --guided
```

**Option B: Deploy Backend via Amplify**

If using Amplify's backend build phase:
1. Ensure `amplify.yml` includes backend phase configuration
2. Set required environment variables in Amplify Console
3. Amplify will build and deploy backend on each push

## 📊 API Endpoints

The backend provides the following REST API endpoints:

### Campaigns (Campañas)
- `GET /v1/campanias/activas` - Get active campaigns
- `POST /v1/campanias` - Create new campaign

### Positions (Puestos)
- `GET /v1/puestos/activos` - Get active positions
- `POST /v1/puestos` - Create new position

### Requirements (Requerimientos)
- `GET /v1/requerimientos/{campania_id}` - Get requirements for a campaign
- `POST /v1/requerimientos` - Create requirement

### Applications (Postulaciones)
- `GET /v1/postulaciones/{requerimiento_id}` - Get applications
- `POST /v1/postulaciones` - Submit application
- `PUT /v1/postulaciones/{postulacion_id}/estado` - Update application status

## 🔧 Local Development

### Frontend Development

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Backend Development

```bash
# Navigate to backend
cd backend/infrastructure

# Install SAM CLI and dependencies
pip install -r ../requirements.txt

# Build SAM application
sam build

# Start local API (runs on http://localhost:3000)
sam local start-api

# Test an endpoint
curl http://localhost:3000/v1/campanias/activas
```

## 📝 Environment Configuration

### Development Environment (`environment.ts`)
- API URL: `http://localhost:3000/v1`
- Used when running `npm start`

### Production Environment (`environment.prod.ts`)
- API URL: From environment variable or AWS API Gateway endpoint
- Used when running `npm run build`

### Update API URL for Production

After deploying the backend via SAM or CloudFormation:

1. Get your API Gateway endpoint URL from AWS Console
2. Update environment.prod.ts or set `API_URL` environment variable in Amplify Console
3. Redeploy frontend: Push code changes or manually trigger rebuild in Amplify Console

## 🗄️ Database Schema

The backend creates the following tables automatically:

- **campanias** - Recruitment campaigns
- **puestos** - Job positions
- **requerimientos** - Position requirements
- **postulaciones** - Job applications
- **usuarios** - User accounts (future feature)

Database includes 17 optimized indexes for performance.

## 🔐 Security

- Lambda functions use IAM roles with least privilege
- Database passwords stored in AWS Secrets Manager
- CORS configured for your frontend domain
- API Gateway throttling and authentication ready
- Structured logging for audit trails

## 📦 Deployment Architecture

```
┌─────────────────────────────────────┐
│   AWS Amplify Console               │
│   (Frontend Hosting & CI/CD)        │
└────────────┬────────────────────────┘
             │
             ├─→ S3 + CloudFront (Static Frontend)
             │
             ├─→ Build & Deploy Scripts
             │
             └─→ Backend Deployment (SAM)
                    │
                    ├─→ Lambda (API Logic)
                    ├─→ API Gateway (REST API)
                    ├─→ RDS (SQL Server Database)
                    └─→ CloudWatch (Logging & Monitoring)
```

## 💰 Estimated Costs

- **Frontend (Amplify)**: $0.99/month per app
- **Lambda**: $0.20 per 1M requests + $0.0000166667 per GB-second
- **API Gateway**: $3.50 per million API calls
- **RDS (db.t3.micro)**: ~$10/month
- **S3 & CloudFront**: ~$1-5/month depending on traffic

**Estimated Total**: $30-50/month for moderate usage

## 🆘 Troubleshooting

### Frontend doesn't connect to backend
- Check `API_URL` in environment.prod.ts
- Verify API Gateway is deployed and accessible
- Check CORS settings in backend Lambda

### Build fails in Amplify
- Check Node.js version (requires 18+)
- Verify package.json dependencies are correct
- Check build logs in Amplify Console for details

### Backend deployment fails
- Ensure AWS credentials are configured
- Check database connectivity parameters
- Verify VPC and subnet configurations
- Review CloudFormation stack events for errors

## 📞 Support

For issues or questions:
1. Check AWS Amplify documentation: https://aws.amazon.com/amplify/
2. Review Lambda logs in CloudWatch Console
3. Test API endpoints manually with curl or Postman

## 📄 License

This project is part of the Recruitment Management System by mcontrerasmalpar-pixel.
