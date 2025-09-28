"""
Registry-specific exceptions for the mcode_translator module.
"""

from ..exceptions import HeySolError


class RegistryError(HeySolError):
    """Base exception for registry operations."""

    pass


class InstanceNotFoundError(RegistryError):
    """Raised when a memory instance is not found in the registry."""

    pass


class OperationError(RegistryError):
    """Raised when a registry operation fails."""

    pass


class InstanceConflictError(RegistryError):
    """Raised when there's a conflict between memory instances."""

    pass


class ValidationError(RegistryError):
    """Raised when registry operation parameters are invalid."""

    pass
