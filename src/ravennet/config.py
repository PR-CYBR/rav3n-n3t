"""
Configuration management for RavenNet.
"""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class Config:
    """Configuration manager for RavenNet orchestrator."""

    DEFAULT_CONFIG = {
        "pipelines": {
            "huginn": {
                "enabled": True,
                "timeout": 3600,
                "retry_count": 3,
            },
            "muninn": {
                "enabled": True,
                "timeout": 3600,
                "retry_count": 3,
            },
        },
        "output": {
            "directory": "./reports",
            "archive": True,
            "format": "json",
        },
        "notifications": {
            "on_failure": True,
            "on_success": False,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to YAML configuration file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()

        if config_path:
            self.load_from_file(config_path)

        self.load_from_env()

    def load_from_file(self, config_path: str) -> None:
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file
        """
        path = Path(config_path)
        if path.exists():
            with open(path, "r") as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_config(file_config)

    def load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Pipeline configurations
        if os.getenv("RAVENNET_HUGINN_ENABLED"):
            self.config["pipelines"]["huginn"]["enabled"] = (
                os.getenv("RAVENNET_HUGINN_ENABLED").lower() == "true"
            )

        if os.getenv("RAVENNET_MUNINN_ENABLED"):
            self.config["pipelines"]["muninn"]["enabled"] = (
                os.getenv("RAVENNET_MUNINN_ENABLED").lower() == "true"
            )

        # Output directory
        if os.getenv("RAVENNET_OUTPUT_DIR"):
            self.config["output"]["directory"] = os.getenv("RAVENNET_OUTPUT_DIR")

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """
        Recursively merge new configuration into existing config.

        Args:
            new_config: New configuration dictionary to merge
        """

        def merge_dict(base: Dict, update: Dict) -> Dict:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
            return base

        merge_dict(self.config, new_config)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., "pipelines.huginn.enabled")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., "pipelines.huginn.enabled")
            value: Value to set
        """
        keys = key.split(".")
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Get full configuration as dictionary.

        Returns:
            Configuration dictionary
        """
        return self.config.copy()
