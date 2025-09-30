"""
Pydantic models for HeySol API responses.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


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

    @field_validator('episodes', mode='before')
    @classmethod
    def convert_episodes_to_dict(cls, v: Any) -> Any:
        """Convert episode strings to dictionaries if needed."""
        if not v:
            return v

        result = []
        for episode in v:
            if isinstance(episode, str):
                # Try to parse as JSON, if that fails, create a simple dict
                try:
                    import json
                    result.append(json.loads(episode))
                except (json.JSONDecodeError, ValueError):
                    # If it's not valid JSON, create a simple dict with the string as content
                    result.append({"content": episode, "source": "unknown"})
            elif isinstance(episode, dict):
                result.append(episode)
            else:
                # For other types, convert to string and wrap in dict
                result.append({"content": str(episode), "source": "unknown"})

        return result


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
    available_methods: List[str] = Field(
        default_factory=list, description="Available check methods"
    )
    recent_logs_count: Optional[int] = Field(default=None, description="Recent logs count")
    search_status: Optional[str] = Field(default=None, description="Search availability status")


class WebhookInfo(BaseModel):
    """Webhook information model."""

    id: str = Field(..., description="Webhook ID")
    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(default_factory=list, description="Webhook events")
    active: bool = Field(default=True, description="Webhook active status")
    created_at: Optional[str] = Field(default=None, description="Creation timestamp")
