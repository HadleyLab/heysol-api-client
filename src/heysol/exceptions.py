class HeySolError(Exception):
    pass


class AuthenticationError(HeySolError):
    pass


class ValidationError(HeySolError):
    pass


class ConnectionError(HeySolError):
    pass


class RateLimitError(HeySolError):
    pass


def validate_api_key_format(api_key: str) -> None:
    api_key_stripped = api_key.strip()
    if not api_key_stripped.startswith("rc_pat_"):
        raise ValidationError(
            "Invalid API key format: Only keys starting with 'rc_pat_' are accepted by this client."
        )
    if len(api_key_stripped) < 40 or len(api_key_stripped) > 60:
        raise ValidationError(
            f"Invalid API key length ({len(api_key_stripped)} characters). rc_pat_ API keys must be between 40 and 60 characters long."
        )
    if "#" in api_key or " #" in api_key:
        raise ValidationError(
            "Invalid API key: Contains comment character '#'. Check your .env file - remove any comments after the API key value."
        )
