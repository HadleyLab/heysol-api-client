"""
Pydantic models for HeySol API client.

This module provides structured data models for API requests, responses,
and configuration using Pydantic for automatic validation and type safety.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict

# Default constants (matching config.py)
DEFAULT_BASE_URL = "https://core.heysol.ai/api/v1"
DEFAULT_SOURCE = "heysol-api-client"
DEFAULT_MCP_URL = f"https://core.heysol.ai/api/v1/mcp?source={DEFAULT_SOURCE}"
DEFAULT_PROFILE_URL = "https://core.heysol.ai/api/profile"


class HeySolConfig(BaseModel):
    """Configuration model for HeySol client initialization."""

    api_key: Optional[str] = Field(default=None, description="HeySol API key for authentication")
    base_url: str = Field(default=DEFAULT_BASE_URL, description="Base URL for API endpoints")
    mcp_url: str = Field(default=DEFAULT_MCP_URL, description="MCP endpoint URL")
    profile_url: str = Field(default=DEFAULT_PROFILE_URL, description="Profile endpoint URL")
    source: str = Field(default=DEFAULT_SOURCE, description="Default source identifier")
    timeout: int = Field(default=60, ge=1, le=300, description="Request timeout in seconds")

    @field_validator('api_key')
    @classmethod
    def validate_api_key_format(cls, v: Optional[str]) -> Optional[str]:
        """Validate API key format if provided."""
        if v is not None and not v.startswith("rc_pat_"):
            raise ValueError("API key must start with 'rc_pat_'")
        return v

    @classmethod
    def from_env(cls) -> "HeySolConfig":
        """Create configuration from environment variables."""
        import os

        timeout_str = os.getenv("HEYSOL_TIMEOUT")
        timeout = int(timeout_str) if timeout_str else 60

        return cls(
            api_key=os.getenv("HEYSOL_API_KEY"),
            base_url=os.getenv("HEYSOL_BASE_URL") or DEFAULT_BASE_URL,
            mcp_url=os.getenv("HEYSOL_MCP_URL") or DEFAULT_MCP_URL,
            profile_url=os.getenv("HEYSOL_PROFILE_URL") or DEFAULT_PROFILE_URL,
            source=os.getenv("HEYSOL_SOURCE") or DEFAULT_SOURCE,
            timeout=timeout,
        )


# API Request Models
class IngestRequest(BaseModel):
    """Request model for data ingestion."""

    episode_body: str = Field(..., min_length=1, description="Content to ingest", alias="episodeBody")
    reference_time: str = Field(default="2023-11-07T05:31:56Z", description="Reference timestamp", alias="referenceTime")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    source: str = Field(..., min_length=1, description="Source identifier")
    session_id: str = Field(default="", description="Session identifier", alias="sessionId")
    space_id: Optional[str] = Field(default=None, description="Target space ID", alias="spaceId")

    model_config = ConfigDict(validate_by_name=True)


class SearchRequest(BaseModel):
    """Request model for memory search."""

    query: str = Field(..., min_length=1, description="Search query")
    space_ids: List[str] = Field(default_factory=list, description="Space IDs to search in")
    include_invalidated: bool = Field(default=False, description="Include invalidated memories")


class CreateSpaceRequest(BaseModel):
    """Request model for creating a new space."""

    name: str = Field(..., min_length=1, description="Space name")
    description: str = Field(default="", description="Space description")


class UpdateSpaceRequest(BaseModel):
    """Request model for updating a space."""

    name: Optional[str] = Field(default=None, min_length=1, description="New space name")
    description: Optional[str] = Field(default=None, description="New space description")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class RegisterWebhookRequest(BaseModel):
    """Request model for webhook registration."""

    url: str = Field(..., description="Webhook URL")
    secret: str = Field(..., min_length=1, description="Webhook secret")


class UpdateWebhookRequest(BaseModel):
    """Request model for webhook updates."""

    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(default_factory=list, description="Webhook events")
    secret: str = Field(..., min_length=1, description="Webhook secret")
    active: bool = Field(default=True, description="Webhook active status")

    @field_validator('events')
    @classmethod
    def validate_events(cls, v: List[str]) -> List[str]:
        """Validate that events list is not empty."""
        if not v:
            raise ValueError("Events list cannot be empty")
        return v


# API Response Models
class SpaceInfo(BaseModel):
    """Space information model."""

    id: str = Field(..., description="Space ID")
    name: str = Field(..., description="Space name")
    description: str = Field(default="", description="Space description")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
    updated_at: Optional[str] = Field(default=None, description="Last update timestamp")


class LogEntry(BaseModel):
    """Log entry model."""

    id: str = Field(..., description="Log entry ID")
    ingest_text: Optional[str] = Field(default=None, description="Ingested text content")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional data")
    time: Optional[str] = Field(default=None, description="Timestamp")
    source: Optional[str] = Field(default=None, description="Source identifier")


class SearchResult(BaseModel):
    """Search result model."""

    episodes: List[Dict[str, Any]] = Field(default_factory=list, description="Found episodes")
    total_count: Optional[int] = Field(default=None, description="Total result count")


class UserProfile(BaseModel):
    """User profile model."""

    id: Optional[str] = Field(default=None, description="User ID")
    email: Optional[str] = Field(default=None, description="User email")
    name: Optional[str] = Field(default=None, description="User name")
    created_at: Optional[str] = Field(default=None, description="Account creation date")


class IngestionStatus(BaseModel):
    """Ingestion status model."""

    ingestion_status: str = Field(default="unknown", description="Current ingestion status")
    recommendations: List[str] = Field(default_factory=list, description="Status recommendations")
    available_methods: List[str] = Field(default_factory=list, description="Available check methods")
    recent_logs_count: Optional[int] = Field(default=None, description="Recent logs count")
    search_status: Optional[str] = Field(default=None, description="Search availability status")


class WebhookInfo(BaseModel):
    """Webhook information model."""

    id: str = Field(..., description="Webhook ID")
    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(default_factory=list, description="Webhook events")
    active: bool = Field(default=True, description="Webhook active status")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")


# Export all models
__all__ = [
    "HeySolConfig",
    "IngestRequest",
    "SearchRequest",
    "CreateSpaceRequest",
    "UpdateSpaceRequest",
    "RegisterWebhookRequest",
    "UpdateWebhookRequest",
    "SpaceInfo",
    "LogEntry",
    "SearchResult",
    "UserProfile",
    "IngestionStatus",
    "WebhookInfo",
]