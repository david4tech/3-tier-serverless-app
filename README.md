# 3-Tier Serverless Pokemon Application

A complete serverless application built with AWS services, featuring a React frontend, Lambda backend, and DynamoDB database.

## Architecture

- **Frontend**: React app hosted on S3 with CloudFront distribution
- **Backend**: Python Lambda functions with API Gateway
- **Database**: DynamoDB tables for Pokemon data storage
- **Infrastructure**: AWS CDK for Infrastructure as Code

## Project Structure

```
3-tier-serverless-app/
├── backend/           # Lambda functions and API Gateway
│   ├── lambda/        # Lambda function code
│   ├── app.py         # CDK stack for backend
│   └── requirements.txt
├── frontend/          # React application
│   ├── src/           # React source code
│   ├── public/        # Static assets
│   ├── app.py         # CDK stack for frontend
│   └── package.json
├── database/          # Database schema and CDK
│   ├── app.py         # CDK stack for database
│   ├── schema.py      # Database schema documentation
│   └── requirements.txt
└── package.json       # Root package with scripts
```

## Local Development Setup

### Prerequisites
- Node.js 18+
- Python 3.9+
- AWS CLI configured
- AWS CDK installed (`npm install -g aws-cdk`)

### Quick Start

1. **Install all dependencies**:
   ```bash
   npm run install-all
   ```

2. **Deploy database first**:
   ```bash
   npm run deploy-database
   ```

3. **Deploy backend**:
   ```bash
   npm run deploy-backend
   ```

4. **Build and deploy frontend**:
   ```bash
   npm run deploy-frontend
   ```

### Local Development

1. **Start backend locally** (for development):
   ```bash
   npm run dev-backend
   ```

2. **Start frontend locally**:
   ```bash
   npm run dev-frontend
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:3001

## API Endpoints

- `GET /pokemons` - Get all Pokemon
- `GET /pokemons/{id}` - Get specific Pokemon
- `POST /pokemons` - Create new Pokemon
- `PUT /pokemons/{id}` - Update Pokemon
- `DELETE /pokemons/{id}` - Delete Pokemon

## Database Schema

### Pokemon Table
- `id` (String) - Primary key
- `name` (String) - Pokemon name
- `type` (String) - Pokemon type
- `level` (Number) - Pokemon level
- `hp` (Number) - Hit points

### Additional Tables
- `PokemonTypesTable` - Type reference data
- `PokemonAbilitiesTable` - Abilities reference data
- `PokemonStatsTable` - Detailed statistics

## Deployment

### Individual Components
```bash
npm run deploy-database  # Deploy database stack
npm run deploy-backend   # Deploy backend stack
npm run deploy-frontend  # Deploy frontend stack
```

### All at Once
```bash
npm run deploy-all
```

### Cleanup
```bash
npm run destroy-all
```

## Environment Variables

For local development, create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=your-api-gateway-url
```

## Features

- ✅ Complete CRUD operations for Pokemon
- ✅ Responsive React frontend
- ✅ Serverless backend with Lambda
- ✅ NoSQL database with DynamoDB
- ✅ Infrastructure as Code with CDK
- ✅ CORS enabled for cross-origin requests
- ✅ CloudFront distribution for global delivery
- ✅ Local development support

## Technologies Used

- **Frontend**: React, Axios, CSS3
- **Backend**: Python, AWS Lambda, API Gateway
- **Database**: AWS DynamoDB
- **Infrastructure**: AWS CDK (Python)
- **Hosting**: AWS S3, CloudFront
- **Development**: Node.js, npm scripts