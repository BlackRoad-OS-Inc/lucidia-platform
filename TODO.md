# Lucidia Platform — TODO

> BlackRoad OS, Inc. — Proprietary
> Last updated: 2026-03-21

---

## [RC] Priority — Revenue Critical

- [ ] [RC] Stripe integration — connect payment links to Pro ($20/mo) and Enterprise ($99/mo) checkout flows
- [ ] [RC] User authentication — implement Clerk sign-in/sign-up with session persistence
- [ ] [RC] Subscription gating — enforce plan limits (100 req/day free, unlimited pro)
- [ ] [RC] Billing portal — allow users to manage subscription, update payment, view invoices
- [ ] [RC] Free trial flow — 14-day Pro trial with automatic downgrade
- [ ] [RC] Usage metering — track daily requests per user, enforce limits
- [ ] [RC] Onboarding flow — first-time user experience with project creation wizard

## [RC] Core Features

- [ ] [RC] Memory Engine v2 — persistent knowledge graph with cross-project connections
- [ ] [RC] Chat interface — real-time WebSocket chat with agent responses
- [ ] [RC] Code execution sandbox — secure sandboxed environments for Python, Node.js, Rust, Go
- [ ] [RC] Ghost Mode — autonomous background task execution with progress tracking
- [ ] [RC] One-click deploy — deploy projects to BlackRoad Edge with DNS + TLS
- [ ] [RC] Visual Intention Engine — map user intent to executable plans with visual flowcharts
- [ ] [RC] Project CRUD — create, read, update, delete projects with file management

## [RC] Cognitive Agents

- [ ] [RC] Curator agent — context retrieval and memory search optimization
- [ ] [RC] Analyzer agent — static analysis, security scanning, performance profiling
- [ ] [RC] Planner agent — task decomposition, dependency graphing, effort estimation
- [ ] [RC] Bridge agent — cross-project knowledge linking and context transfer
- [ ] [RC] Identity Keeper agent — style enforcement, brand consistency, naming conventions
- [ ] [RC] Explainer agent — documentation generation, code explanation, ADRs
- [ ] [RC] Agent coordination — multi-agent pipeline with shared context via RoundTrip

## Frontend — Landing Page

- [x] Hero section with gradient text and metrics
- [x] Features grid (6 features with icons and descriptions)
- [x] How It Works (4-step process)
- [x] Code demo with typing animation
- [x] Cognitive Agents showcase (6 agents)
- [x] Memory showcase with visual graph
- [x] Pricing cards (Free, Pro, Enterprise)
- [x] RoundTrip integration widget
- [x] Testimonials section
- [x] CTA section with gradient border
- [x] Responsive design (mobile, tablet, desktop)
- [ ] SEO meta tags and Open Graph images
- [ ] Analytics tracking (PostHog or Plausible)
- [ ] A/B testing for pricing page CTAs

## Frontend — App Dashboard

- [x] Sidebar navigation (Dashboard, Projects, Memory, Agents, Code, Deploy, Settings)
- [x] Stats row (projects, memory nodes, deployments, agent tasks)
- [x] Project list with status indicators
- [x] Agent status grid (6 agents with online/idle/offline states)
- [x] Chat panel with message history and typing indicator
- [x] Command shortcuts (/deploy, /ghost, /memory, /agents)
- [ ] Project detail view with file tree
- [ ] Memory graph visualization (D3.js or Cytoscape)
- [ ] Agent configuration panel
- [ ] Deploy status and logs view
- [ ] Settings page (profile, billing, API keys)
- [ ] Dark/light theme toggle (dark is default)

## Frontend — Pricing Page

- [x] 3-tier pricing cards (Free, Pro, Enterprise)
- [x] Monthly/annual billing toggle with 20% discount
- [x] Feature comparison table (20+ features across 5 categories)
- [x] FAQ section (10 questions)
- [x] Responsive design
- [ ] Stripe checkout integration (actual payment links)
- [ ] Plan upgrade/downgrade flow
- [ ] Team seat management for Enterprise

## Backend — API

- [x] Health check endpoint with service status
- [x] Agent list/detail endpoints with filtering
- [x] Project list/detail endpoints with filtering and pagination
- [x] Chat endpoint with multi-agent pipeline
- [x] Memory query endpoint with full-text search
- [x] Platform statistics endpoint
- [ ] Database integration (PostgreSQL on Alice)
- [ ] Authentication middleware (Clerk JWT verification)
- [ ] Rate limiting middleware (Redis on Alice)
- [ ] WebSocket support for real-time chat
- [ ] File upload and management
- [ ] Code execution engine integration
- [ ] Memory graph persistence (Qdrant on Alice)
- [ ] Deploy engine integration (BlackRoad Edge)
- [ ] Webhook handlers (Stripe, Clerk)
- [ ] API key management for Enterprise users

## Infrastructure

- [ ] DNS setup — lucidia.ai, app.lucidia.ai, api.lucidia.ai
- [ ] TLS certificates via Caddy on Gematria
- [ ] Deploy to BlackRoad Edge (Octavia workers)
- [ ] PostgreSQL schema and migrations
- [ ] Redis caching layer
- [ ] Qdrant vector store for memory embeddings
- [ ] Docker Compose for local development
- [ ] CI/CD pipeline via Gitea Actions
- [ ] Health monitoring and alerting
- [ ] Backup and disaster recovery

## Documentation

- [ ] API reference (auto-generated from FastAPI)
- [ ] Getting started guide
- [ ] Agent configuration guide
- [ ] Memory system documentation
- [ ] Self-hosted deployment guide (Enterprise)
- [ ] Contributing guidelines update

---

**BlackRoad OS — Pave Tomorrow.**
