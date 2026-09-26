# Allow modern type hint syntax on earlier verisons of Python < 3.9
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from utils.console.console_utils import warn, fail, error, info

# =====================================================================================
#                                 File Managing Helpers
# =====================================================================================


# ======
# Guards
# ======
def is_file_available(path: str) -> bool:
    """Returns True if a file exists at the given path, False otherwise."""
    if not os.path.exists(path):
        return False
    return True


def _is_dictionary(config: dict) -> bool:
    """Returns True if the given object is a dictionary, False otherwise."""
    if not isinstance(config, dict):
        return False
    return True


# ==========
# Validation
# ==========
def ensure_is_dictionary(data: Any, key: str, path: str) -> None:
    """Raises a ValueError if data is not a dictionary.

    Used to enforce that a YAML section resolves to a mapping, not a scalar or list.
    """
    if not _is_dictionary(data):
        raise ValueError(f"'{key}' must be a dictionary in {path}. ")


# ===============
# Path Resolution
# ===============
def construct_file_path(dir: str, file: str, subdir: str) -> str:
    """Constructs an absolute file path from a directory, subdirectory, and filename.

    If file is already an absolute path, it is returned as-is.
    Relative paths with separators are rejected, only plain filenames are accepted.
    """
    if os.path.isabs(file):
        return file

    if "/" in file or "\\" in file:
        raise ValueError(
            f"Input must be an absolute path or a filename only, got: {file}"
        )

    return os.path.join(dir, subdir, file)


# ================
# Load YAML Data
# ================
def _load_yaml_data(path: str) -> dict[str, Any]:
    """Loads and parses a YAML file, returning its contents as a dictionary.

    Returns an empty dict if the file is empty.
    Raises FileNotFoundError if the path does not exist.
    Raises TypeError if the YAML root is not a mapping.
    Raises yaml.YAMLError if the file cannot be parsed.
    """
    config_file = Path(path)

    if not config_file.exists():
        raise FileNotFoundError(path)

    try:
        with config_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data is None:
            print(warn(f"YAML file is empty: {path}"))
            return {}

        if not isinstance(data, dict):
            print(error(f"YAML root must be a dictionary: {path}"))
            raise TypeError(f"YAML root must be a dictionary: {path}")

        return data

    except yaml.YAMLError as e:
        print(fail(f"Failed to parse YAML file: {path}\n{e}"))
        raise


# =====================================================================================
#                                  Config Loading
# =====================================================================================
def get_yaml_config_data(
    dir: str, config_file: str, config_subdir: str = "config"
) -> dict[str, Any]:
    """Resolves and loads a YAML configuration file, returning its contents as a dictionary.

    Raises FileNotFoundError if the file does not exist at the resolved path.
    """
    config_path = get_file_path(dir, config_file, config_subdir)
    print(info(f"Loading config: {config_path}"))
    config_data = _load_yaml_data(config_path)
    return config_data


def get_file_path(dir: str, file: str, config_subdir: str = "config") -> str:
    """Resolves and validates the absolute path to a file.

    Raises FileNotFoundError if the file does not exist at the resolved path.
    """
    file_path = construct_file_path(dir, file, config_subdir)

    if not is_file_available(file_path):
        print(error(f"File not found: {file_path}"))
        raise FileNotFoundError(f"File not found at: {file_path}")

    return file_path
