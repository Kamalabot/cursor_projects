from crewai.tools import BaseTool
import redis
from typing import Optional, Union
from pydantic import Field, ConfigDict

class RedisCacheTool(BaseTool):
    name: str = "Redis Cache Tool"
    description: str = """
    Stores key-value data in Redis cache.
    
    Parameters:
    - key: The identifier for storing the data (e.g., "user_id", "session_token")
    - value: The data to be stored (e.g., "12345", "active")
    - expiry: (Optional) Time in seconds before the key expires
    
    Examples:
    - Store user preference: _run("user_theme", "dark_mode")
    - Store session with expiry: _run("session_123", "active", 3600)
    - Store JSON-like data: _run("user_settings", "{'theme': 'dark', 'notifications': 'on'}")
    """
    redis_client: redis.Redis = Field(default=None, exclude=True)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None):
        redis_client = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True
        )
        super().__init__(redis_client=redis_client)

    def _run(self, key: str, value: Union[str, int, float], expiry: Optional[int] = None) -> str:
        """
        Store data in Redis cache with optional expiration.

        Args:
            key (str): The key under which to store the value.
                Examples:
                - "user_123:preferences"
                - "session_token:abc123"
                - "cache:daily_stats"
            
            value (Union[str, int, float]): The value to store.
                Examples:
                - "dark_mode"
                - 42
                - "{'name': 'John', 'age': 30}"
            
            expiry (Optional[int]): Time in seconds after which the key will expire.
                Examples:
                - 3600 (1 hour)
                - 86400 (1 day)
                - None (no expiration)

        Returns:
            str: A message indicating the success or failure of the operation.

        Examples:
            >>> tool._run("user:theme", "dark_mode")
            "Successfully stored key 'user:theme' with value 'dark_mode'"
            
            >>> tool._run("session:123", "active", 3600)
            "Successfully stored key 'session:123' with value 'active' and 3600 seconds expiry"
        """
        try:
            # Validate inputs
            if not key or not isinstance(key, str):
                return "Error: Key must be a non-empty string"
            
            if value is None:
                return "Error: Value cannot be None"

            # Convert value to string if it's not already
            value_str = str(value)

            # Store in Redis with or without expiry
            if expiry:
                if not isinstance(expiry, int) or expiry <= 0:
                    return "Error: Expiry must be a positive integer"
                self.redis_client.setex(key, expiry, value_str)
                return f"Successfully stored key '{key}' with value '{value_str}' and {expiry} seconds expiry"
            else:
                self.redis_client.set(key, value_str)
                return f"Successfully stored key '{key}' with value '{value_str}'"

        except Exception as e:
            return f"Error storing data in Redis: {str(e)}"
