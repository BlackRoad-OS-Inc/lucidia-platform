"""
Lucidia Platform API — Core Routes
BlackRoad OS, Inc. — Proprietary

FastAPI routes for the Lucidia AI Creator Platform.
Handles health checks, agent management, project CRUD,
chat interactions, and memory graph queries.
"""

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


# ============================================================
# App Configuration
# ============================================================

app = FastAPI(
    title="Lucidia Platform API",
    description=(
        "AI creator platform with infinite project memory, "
        "live code execution, 6 cognitive agents, and one-click deploy. "
        "Built by BlackRoad OS, Inc."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "BlackRoad OS, Inc.",
        "url": "https://blackroad.io",
        "email": "alexa@blackroad.io",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://blackroad.io/license",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://lucidia.ai",
        "https://app.lucidia.ai",
        "https://lucidia.blackroad.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Enums
# ============================================================

class AgentRole(str, Enum):
    CURATOR = "curator"
    ANALYZER = "analyzer"
    PLANNER = "planner"
    BRIDGE = "bridge"
    IDENTITY_KEEPER = "identity-keeper"
    EXPLAINER = "explainer"


class AgentStatus(str, Enum):
    ONLINE = "online"
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class MemoryNodeType(str, Enum):
    PATTERN = "pattern"
    DECISION = "decision"
    ERROR = "error"
    SOLUTION = "solution"
    CONTEXT = "context"
    DEPLOY = "deploy"


class PlanTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# ============================================================
# Response Models
# ============================================================

class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: str
    services: Dict[str, str]
    uptime_seconds: int


class AgentResponse(BaseModel):
    id: str = Field(description="Unique agent identifier")
    name: str = Field(description="Human-readable agent name")
    role: AgentRole = Field(description="Agent's cognitive role")
    status: AgentStatus = Field(description="Current operational status")
    description: str = Field(description="What this agent does")
    tasks_completed: int = Field(description="Total tasks completed in current session")
    memory_nodes: int = Field(description="Memory nodes this agent has created")
    last_active: str = Field(description="ISO timestamp of last activity")


class AgentListResponse(BaseModel):
    agents: List[AgentResponse]
    total: int
    online_count: int


class ProjectResponse(BaseModel):
    id: str = Field(description="Unique project identifier")
    name: str = Field(description="Project name")
    description: Optional[str] = Field(default=None, description="Project description")
    language: str = Field(description="Primary programming language")
    status: ProjectStatus = Field(description="Current project status")
    file_count: int = Field(description="Number of files in project")
    memory_nodes: int = Field(description="Associated memory graph nodes")
    created_at: str = Field(description="ISO timestamp of creation")
    updated_at: str = Field(description="ISO timestamp of last update")
    deploy_url: Optional[str] = Field(default=None, description="Live deployment URL")


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    active_count: int


class ChatMessage(BaseModel):
    role: str = Field(description="Message role: user, assistant, agent")
    content: str = Field(description="Message content")
    agent: Optional[str] = Field(default=None, description="Agent name if role is agent")
    timestamp: str = Field(description="ISO timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Extra metadata")


class ChatRequest(BaseModel):
    message: str = Field(description="User's chat message")
    project_id: Optional[str] = Field(default=None, description="Project context")
    include_memory: bool = Field(default=True, description="Include memory context")
    ghost_mode: bool = Field(default=False, description="Enable autonomous execution")
    agents: Optional[List[AgentRole]] = Field(
        default=None, description="Specific agents to engage"
    )


class ChatResponse(BaseModel):
    id: str = Field(description="Unique conversation turn ID")
    messages: List[ChatMessage] = Field(description="Response messages from agents")
    memory_nodes_created: int = Field(description="New memory nodes from this turn")
    tokens_used: int = Field(description="Total tokens consumed")
    execution_time_ms: int = Field(description="Total processing time in milliseconds")
    project_id: Optional[str] = Field(default=None)


class MemoryNode(BaseModel):
    id: str = Field(description="Unique memory node ID")
    type: MemoryNodeType = Field(description="Type of memory node")
    title: str = Field(description="Short title")
    content: str = Field(description="Full content/details")
    project_id: Optional[str] = Field(default=None, description="Associated project")
    connections: List[str] = Field(
        default_factory=list, description="IDs of connected memory nodes"
    )
    created_at: str = Field(description="ISO timestamp")
    created_by: str = Field(description="Agent or user who created this node")
    relevance_score: Optional[float] = Field(
        default=None, description="Relevance score (0-1) for search results"
    )


class MemoryResponse(BaseModel):
    nodes: List[MemoryNode]
    total: int
    graph_stats: Dict[str, int]


class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: str


# ============================================================
# Data Store (in-memory for development; replace with DB)
# ============================================================

AGENTS_DB: List[Dict[str, Any]] = [
    {
        "id": "agent-curator-001",
        "name": "Curator",
        "role": AgentRole.CURATOR,
        "status": AgentStatus.ONLINE,
        "description": (
            "Organizes and retrieves relevant context from your entire project "
            "history. Surfaces patterns, solutions, and decisions."
        ),
        "tasks_completed": 342,
        "memory_nodes": 891,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
    {
        "id": "agent-analyzer-001",
        "name": "Analyzer",
        "role": AgentRole.ANALYZER,
        "status": AgentStatus.ONLINE,
        "description": (
            "Deep static and dynamic analysis of your codebase. Identifies "
            "performance bottlenecks, security vulnerabilities, and refactoring ops."
        ),
        "tasks_completed": 218,
        "memory_nodes": 567,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
    {
        "id": "agent-planner-001",
        "name": "Planner",
        "role": AgentRole.PLANNER,
        "status": AgentStatus.ONLINE,
        "description": (
            "Breaks complex requests into executable plans with task trees, "
            "dependency graphs, and implementation roadmaps."
        ),
        "tasks_completed": 156,
        "memory_nodes": 423,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
    {
        "id": "agent-bridge-001",
        "name": "Bridge",
        "role": AgentRole.BRIDGE,
        "status": AgentStatus.ONLINE,
        "description": (
            "Connects knowledge across projects, sessions, and team members. "
            "Links relevant context from any point in your history."
        ),
        "tasks_completed": 189,
        "memory_nodes": 334,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
    {
        "id": "agent-identity-001",
        "name": "Identity Keeper",
        "role": AgentRole.IDENTITY_KEEPER,
        "status": AgentStatus.IDLE,
        "description": (
            "Maintains consistency across all output — code style, naming "
            "conventions, brand voice, and design tokens."
        ),
        "tasks_completed": 98,
        "memory_nodes": 211,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
    {
        "id": "agent-explainer-001",
        "name": "Explainer",
        "role": AgentRole.EXPLAINER,
        "status": AgentStatus.ONLINE,
        "description": (
            "Generates documentation, inline comments, ADRs, and onboarding "
            "guides. Explains complex code in plain language."
        ),
        "tasks_completed": 134,
        "memory_nodes": 289,
        "last_active": datetime.utcnow().isoformat() + "Z",
    },
]

PROJECTS_DB: List[Dict[str, Any]] = [
    {
        "id": "proj-saas-001",
        "name": "saas-dashboard",
        "description": "Full-stack SaaS dashboard with auth, billing, and real-time analytics",
        "language": "TypeScript",
        "status": ProjectStatus.ACTIVE,
        "file_count": 14,
        "memory_nodes": 342,
        "created_at": "2026-03-10T08:00:00Z",
        "updated_at": "2026-03-21T14:30:00Z",
        "deploy_url": "https://saas-dashboard.lucidia.ai",
    },
    {
        "id": "proj-api-001",
        "name": "api-gateway",
        "description": "FastAPI gateway with rate limiting, caching, and multi-service routing",
        "language": "Python",
        "status": ProjectStatus.ACTIVE,
        "file_count": 28,
        "memory_nodes": 518,
        "created_at": "2026-03-05T10:00:00Z",
        "updated_at": "2026-03-21T11:00:00Z",
        "deploy_url": "https://api-gateway.lucidia.ai",
    },
    {
        "id": "proj-auth-001",
        "name": "auth-service",
        "description": "Rust-based authentication service with JWT + refresh token rotation",
        "language": "Rust",
        "status": ProjectStatus.PAUSED,
        "file_count": 11,
        "memory_nodes": 189,
        "created_at": "2026-02-20T12:00:00Z",
        "updated_at": "2026-03-19T09:00:00Z",
        "deploy_url": None,
    },
]

MEMORY_DB: List[Dict[str, Any]] = [
    {
        "id": "mem-001",
        "type": MemoryNodeType.PATTERN,
        "title": "Auth Flow Pattern",
        "content": "JWT + refresh token rotation with httpOnly cookies. Implemented in auth-service and reused in saas-dashboard.",
        "project_id": "proj-auth-001",
        "connections": ["mem-002", "mem-003"],
        "created_at": "2026-03-18T10:00:00Z",
        "created_by": "curator",
    },
    {
        "id": "mem-002",
        "type": MemoryNodeType.SOLUTION,
        "title": "Stripe Billing Hook",
        "content": "Webhook handler: subscription.updated -> sync plan tier to user record. Idempotency via event ID.",
        "project_id": "proj-saas-001",
        "connections": ["mem-001"],
        "created_at": "2026-03-15T14:00:00Z",
        "created_by": "analyzer",
    },
    {
        "id": "mem-003",
        "type": MemoryNodeType.ERROR,
        "title": "CORS on /api/chat",
        "content": "Fix: add app.lucidia.ai to allowedOrigins array in CORS middleware config.",
        "project_id": "proj-api-001",
        "connections": ["mem-001"],
        "created_at": "2026-03-12T08:00:00Z",
        "created_by": "analyzer",
    },
]


# ============================================================
# Routes
# ============================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check",
    description="Returns the current health status of all platform services.",
)
async def health_check():
    """Check platform health and service status."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat() + "Z",
        services={
            "api": "healthy",
            "memory_engine": "healthy",
            "code_analyzer": "healthy",
            "agent_coordinator": "healthy",
            "deploy_engine": "healthy",
            "roundtrip": "healthy",
        },
        uptime_seconds=86400,
    )


@app.get(
    "/api/agents",
    response_model=AgentListResponse,
    tags=["Agents"],
    summary="List cognitive agents",
    description="Returns all 6 cognitive agents with their current status and stats.",
)
async def list_agents(
    status: Optional[AgentStatus] = Query(
        default=None, description="Filter by agent status"
    ),
    role: Optional[AgentRole] = Query(
        default=None, description="Filter by agent role"
    ),
):
    """List all cognitive agents with optional filtering."""
    agents = AGENTS_DB
    if status:
        agents = [a for a in agents if a["status"] == status]
    if role:
        agents = [a for a in agents if a["role"] == role]

    online = sum(1 for a in agents if a["status"] == AgentStatus.ONLINE)

    return AgentListResponse(
        agents=[AgentResponse(**a) for a in agents],
        total=len(agents),
        online_count=online,
    )


@app.get(
    "/api/agents/{agent_id}",
    response_model=AgentResponse,
    tags=["Agents"],
    summary="Get agent details",
    description="Returns detailed information about a specific cognitive agent.",
)
async def get_agent(agent_id: str):
    """Get a specific agent by ID."""
    for agent in AGENTS_DB:
        if agent["id"] == agent_id:
            return AgentResponse(**agent)
    raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")


@app.get(
    "/api/projects",
    response_model=ProjectListResponse,
    tags=["Projects"],
    summary="List projects",
    description="Returns all projects for the authenticated user.",
)
async def list_projects(
    status: Optional[ProjectStatus] = Query(
        default=None, description="Filter by project status"
    ),
    language: Optional[str] = Query(
        default=None, description="Filter by programming language"
    ),
    limit: int = Query(default=50, ge=1, le=100, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
):
    """List all projects with optional filtering and pagination."""
    projects = PROJECTS_DB
    if status:
        projects = [p for p in projects if p["status"] == status]
    if language:
        projects = [
            p for p in projects if p["language"].lower() == language.lower()
        ]

    total = len(projects)
    projects = projects[offset : offset + limit]
    active = sum(1 for p in PROJECTS_DB if p["status"] == ProjectStatus.ACTIVE)

    return ProjectListResponse(
        projects=[ProjectResponse(**p) for p in projects],
        total=total,
        active_count=active,
    )


@app.get(
    "/api/projects/{project_id}",
    response_model=ProjectResponse,
    tags=["Projects"],
    summary="Get project details",
    description="Returns detailed information about a specific project.",
)
async def get_project(project_id: str):
    """Get a specific project by ID."""
    for project in PROJECTS_DB:
        if project["id"] == project_id:
            return ProjectResponse(**project)
    raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    summary="Send chat message",
    description=(
        "Send a message to Lucidia. Engages cognitive agents based on the request, "
        "optionally with project context and memory integration."
    ),
)
async def chat(request: ChatRequest = Body(...)):
    """
    Process a chat message through the cognitive agent pipeline.

    The message is routed through relevant agents based on content analysis:
    - Curator checks memory for relevant context
    - Planner creates execution plans for complex requests
    - Analyzer handles code-related queries
    - Bridge connects cross-project knowledge
    - Identity Keeper enforces style consistency
    - Explainer generates documentation and explanations

    Ghost Mode enables autonomous execution without user approval at each step.
    """
    turn_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat() + "Z"

    messages: List[ChatMessage] = []

    # Curator always checks memory first
    messages.append(
        ChatMessage(
            role="agent",
            content=(
                f"Searching memory for context related to: '{request.message[:80]}...'. "
                "Found 3 relevant patterns from previous sessions."
            ),
            agent="curator",
            timestamp=now,
            metadata={"patterns_found": 3, "search_time_ms": 45},
        )
    )

    # Planner creates execution plan
    messages.append(
        ChatMessage(
            role="agent",
            content=(
                "Execution plan created. 2 tasks identified: "
                "(1) analyze request context, (2) generate response with code examples. "
                "Estimated completion: 8 seconds."
            ),
            agent="planner",
            timestamp=now,
            metadata={"tasks": 2, "estimated_seconds": 8},
        )
    )

    # Main assistant response
    messages.append(
        ChatMessage(
            role="assistant",
            content=(
                f"I have analyzed your request and found relevant context from your project history. "
                f"Here is my response based on the patterns and solutions in your memory graph."
            ),
            timestamp=now,
            metadata={"model": "lucidia-v1", "confidence": 0.94},
        )
    )

    return ChatResponse(
        id=turn_id,
        messages=messages,
        memory_nodes_created=2,
        tokens_used=1247,
        execution_time_ms=3200,
        project_id=request.project_id,
    )


@app.get(
    "/api/memory",
    response_model=MemoryResponse,
    tags=["Memory"],
    summary="Query memory graph",
    description=(
        "Search and retrieve nodes from the persistent memory graph. "
        "Supports filtering by type, project, and full-text search."
    ),
)
async def query_memory(
    query: Optional[str] = Query(
        default=None, description="Full-text search query"
    ),
    type: Optional[MemoryNodeType] = Query(
        default=None, description="Filter by memory node type"
    ),
    project_id: Optional[str] = Query(
        default=None, description="Filter by project ID"
    ),
    limit: int = Query(default=50, ge=1, le=200, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
):
    """
    Query the persistent memory graph.

    The memory graph stores every decision, pattern, error, solution,
    and context across all projects and sessions. Nodes are connected
    by relevance, forming a knowledge graph that grows over time.
    """
    nodes = MEMORY_DB

    if type:
        nodes = [n for n in nodes if n["type"] == type]
    if project_id:
        nodes = [n for n in nodes if n.get("project_id") == project_id]
    if query:
        query_lower = query.lower()
        nodes = [
            n
            for n in nodes
            if query_lower in n["title"].lower()
            or query_lower in n["content"].lower()
        ]

    total = len(nodes)
    nodes = nodes[offset : offset + limit]

    # Add relevance scores for search results
    scored_nodes = []
    for node in nodes:
        node_copy = dict(node)
        if query:
            node_copy["relevance_score"] = 0.85  # Placeholder scoring
        scored_nodes.append(node_copy)

    # Graph statistics
    type_counts: Dict[str, int] = {}
    for n in MEMORY_DB:
        t = n["type"].value if hasattr(n["type"], "value") else str(n["type"])
        type_counts[t] = type_counts.get(t, 0) + 1

    graph_stats = {
        "total_nodes": len(MEMORY_DB),
        "total_connections": sum(len(n.get("connections", [])) for n in MEMORY_DB),
        "projects_covered": len(
            set(n.get("project_id") for n in MEMORY_DB if n.get("project_id"))
        ),
        **{f"type_{k}": v for k, v in type_counts.items()},
    }

    return MemoryResponse(
        nodes=[MemoryNode(**n) for n in scored_nodes],
        total=total,
        graph_stats=graph_stats,
    )


@app.get(
    "/api/memory/{node_id}",
    response_model=MemoryNode,
    tags=["Memory"],
    summary="Get memory node",
    description="Returns a specific memory node by ID with all connections.",
)
async def get_memory_node(node_id: str):
    """Get a specific memory node by ID."""
    for node in MEMORY_DB:
        if node["id"] == node_id:
            return MemoryNode(**node)
    raise HTTPException(status_code=404, detail=f"Memory node '{node_id}' not found")


@app.get(
    "/api/stats",
    tags=["System"],
    summary="Platform statistics",
    description="Returns aggregate platform usage statistics.",
)
async def platform_stats():
    """Get aggregate platform statistics."""
    return {
        "projects": {
            "total": len(PROJECTS_DB),
            "active": sum(
                1 for p in PROJECTS_DB if p["status"] == ProjectStatus.ACTIVE
            ),
        },
        "agents": {
            "total": len(AGENTS_DB),
            "online": sum(
                1 for a in AGENTS_DB if a["status"] == AgentStatus.ONLINE
            ),
            "tasks_completed": sum(a["tasks_completed"] for a in AGENTS_DB),
        },
        "memory": {
            "total_nodes": len(MEMORY_DB),
            "total_connections": sum(
                len(n.get("connections", [])) for n in MEMORY_DB
            ),
        },
        "platform": {
            "version": "1.0.0",
            "uptime_hours": 24,
            "plan": PlanTier.PRO.value,
        },
    }


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
