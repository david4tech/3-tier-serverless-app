# 3-Tier Serverless Pokemon Application Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                   FRONTEND TIER                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   React App     │    │   Amazon S3     │    │  CloudFront     │             │
│  │                 │───▶│   Static Web    │───▶│   CDN           │             │
│  │  - Pokemon UI   │    │   Hosting       │    │  - Global       │             │
│  │  - CRUD Forms   │    │  - HTML/CSS/JS  │    │    Distribution │             │
│  │  - Pokedex      │    │  - Build Files  │    │  - Edge Caching │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                          │                      │
└─────────────────────────────────────────────────────────┼──────────────────────┘
                                                           │
                                                           │ HTTPS Requests
                                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND TIER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           API Gateway                                       │ │
│  │                                                                             │ │
│  │  GET    /pokemons     ──┐                                                  │ │
│  │  POST   /pokemons     ──┤                                                  │ │
│  │  GET    /pokemons/{id}──┤                                                  │ │
│  │  PUT    /pokemons/{id}──┤                                                  │ │
│  │  DELETE /pokemons/{id}──┘                                                  │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                     │                                           │
│                                     │ Route to specific Lambda                  │
│                                     ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         AWS Lambda Functions                                │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │ │
│  │  │ get_pokemons.py │  │ get_pokemon.py  │  │create_pokemon.py│             │ │
│  │  │                 │  │                 │  │                 │             │ │
│  │  │ GET /pokemons   │  │GET /pokemons/id │  │POST /pokemons   │             │ │
│  │  │ - List all      │  │ - Get single    │  │ - Create new    │             │ │
│  │  │ - Scan table    │  │ - Get item      │  │ - Put item      │             │ │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘             │ │
│  │                                                                             │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                                  │ │
│  │  │update_pokemon.py│  │delete_pokemon.py│                                  │ │
│  │  │                 │  │                 │                                  │ │
│  │  │PUT /pokemons/id │  │DEL /pokemons/id │                                  │ │
│  │  │ - Update item   │  │ - Delete item   │                                  │ │
│  │  │ - Update table  │  │ - Remove from   │                                  │ │
│  │  │                 │  │   table         │                                  │ │
│  │  └─────────────────┘  └─────────────────┘                                  │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                     │                                           │
└─────────────────────────────────────┼───────────────────────────────────────────┘
                                      │
                                      │ DynamoDB Operations
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 DATABASE TIER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                           Amazon DynamoDB                                   │ │
│  │                                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                        PokemonTable                                 │   │ │
│  │  │                                                                     │   │ │
│  │  │  Partition Key: id (String)                                         │   │ │
│  │  │                                                                     │   │ │
│  │  │  Attributes:                                                        │   │ │
│  │  │  - id: UUID string                                                  │   │ │
│  │  │  - name: Pokemon name                                               │   │ │
│  │  │  - type: Pokemon type                                               │   │ │
│  │  │  - image: Sprite URL                                                │   │ │
│  │  │  - pokedexNumber: National Dex number                              │   │ │
│  │  │                                                                     │   │ │
│  │  │  Operations:                                                        │   │ │
│  │  │  - Scan (get all)                                                   │   │ │
│  │  │  - GetItem (get by id)                                              │   │ │
│  │  │  - PutItem (create)                                                 │   │ │
│  │  │  - UpdateItem (update)                                              │   │ │
│  │  │  - DeleteItem (delete)                                              │   │ │
│  │  └─────────────────────────────────────────────────────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                CI/CD PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │  GitHub Repo    │───▶│ GitHub Actions  │───▶│   AWS Account   │             │
│  │                 │    │                 │    │                 │             │
│  │ - Source Code   │    │ - Build & Test  │    │ - Deploy Stacks │             │
│  │ - CDK Stacks    │    │ - CDK Deploy    │    │ - Database      │             │
│  │ - Lambda Code   │    │ - Auto Deploy   │    │ - Backend       │             │
│  │ - React App     │    │   on Push       │    │ - Frontend      │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

Data Flow:
1. User interacts with React app hosted on CloudFront/S3
2. Frontend makes HTTPS requests to API Gateway
3. API Gateway routes requests to specific Lambda functions
4. Lambda functions perform CRUD operations on DynamoDB
5. Results flow back through the same path to the user
6. GitHub Actions automatically deploys changes to AWS
```