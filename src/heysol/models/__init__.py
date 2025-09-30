"""
Pydantic models for HeySol API client.

This package provides structured data models for API requests, responses,
and configuration using Pydantic for automatic validation and type safety.
"""

from .config import HeySolConfig
from .requests import (
    CreateSpaceRequest,
    IngestRequest,
    RegisterWebhookRequest,
    SearchRequest,
    UpdateSpaceRequest,
    UpdateWebhookRequest,
)
from .responses import (
    IngestionStatus,
    LogEntry,
    SearchResult,
    SpaceInfo,
    UserProfile,
    WebhookInfo,
)

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
