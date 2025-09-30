"""
Pydantic models for HeySol API requests.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class IngestRequest(BaseModel):
    """Request model for data ingestion."""

    episode_body: str = Field(
        ..., min_length=1, description="Content to ingest", alias="episodeBody"
    )
    reference_time: str = Field(
        default="2023-11-07T05:31:56Z",
        description="Reference timestamp",
        alias="referenceTime",
    )
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    source: str = Field(..., min_length=1, description="Source identifier")
    session_id: str = Field(default="", description="Session identifier", alias="sessionId")
    space_id: Optional[str] = Field(default=None, description="Target space ID", alias="spaceId")

    model_config = ConfigDict(populate_by_name=True)


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

    url: HttpUrl = Field(..., description="Webhook URL")
    secret: str = Field(..., min_length=1, description="Webhook secret")


class UpdateWebhookRequest(BaseModel):
    """Request model for webhook updates."""

    url: HttpUrl = Field(..., description="Webhook URL")
    events: List[str] = Field(default_factory=list, description="Webhook events")
    secret: str = Field(..., min_length=1, description="Webhook secret")
    active: bool = Field(default=True, description="Webhook active status")

    @field_validator("events")
    @classmethod
    def validate_events(cls, v: List[str]) -> List[str]:
        """Validate that events list is not empty."""
        if not v:
            raise ValueError("Events list cannot be empty")
        return v
