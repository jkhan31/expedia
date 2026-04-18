"""
Shared utilities for social content automation
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List


def load_yaml(filepath: str) -> Dict[str, Any]:
    """Load YAML configuration file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON configuration file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(filepath: str, data: Dict[str, Any]):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def create_directory(path: str):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)


def get_output_dir(project_name: str, platform: str) -> str:
    """Get output directory for a project and platform"""
    return f"outputs/{project_name}/{platform}"


def ensure_output_dirs(project_name: str, platforms: List[str]):
    """Create output directories for all platforms"""
    for platform in platforms:
        create_directory(get_output_dir(project_name, platform))


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate project configuration"""
    required_fields = ['project_name', 'carousels', 'website_link']
    for field in required_fields:
        if field not in config:
            print(f"Error: Missing required field '{field}' in config")
            return False
    return True


def get_hex_color(color_name: str, branding_config: Dict) -> str:
    """Get hex color from branding config"""
    color_map = branding_config.get('branding', {})
    return color_map.get(f"{color_name}_color", "#000000")


def log_progress(step: str, status: str = "✓"):
    """Log progress message"""
    print(f"[{status}] {step}")


def log_error(step: str, error: Exception):
    """Log error message"""
    print(f"[✗] {step}: {str(error)}")
