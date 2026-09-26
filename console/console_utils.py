# Allow modern type hint syntax on earlier verisons of Python < 3.9
from __future__ import annotations

import shlex
import textwrap
from typing import Any

# ===========
# ANSI Codes
# ===========
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
RED = "\033[31m"
PURPLE = "\033[38;5;129m"
DARK_PINK = "\033[38;5;125m"
DEFAULT_WIDTH = 60

OK = "🟢"
INFO = "🔵"
WARN = "🟡"
ERR = "🔴"


# =======
# Helpers
# =======
def _box_width(text: str, minimum: int = DEFAULT_WIDTH) -> int:
    """Returns a box width large enough to fit text, with a minimum floor."""
    return max(minimum, len(text) + 4)


def separator(char: str = "─", width: int = DEFAULT_WIDTH) -> str:
    """Returns a separator string"""
    return char * width


# =======
# Banners
# =======
def banner(text: str) -> str:
    """Large bordered banner that scales to text and centers."""
    padding = 6
    width = max(60, len(text) + padding)

    return (
        f"\n{BOLD}{CYAN}"
        f"╔{'═' * width}╗\n"
        f"║{text.center(width)}║\n"
        f"╚{'═' * width}╝"
        f"{RESET}\n"
    )


# =====
# Boxes
# =====
def error_box(title: str, text: str) -> str:
    """Returns a red bordered box with a header and auto-wrapped message text."""
    width = DEFAULT_WIDTH

    # Header
    res = f"\n{BOLD}{RED}╔{'═' * width}╗\n"
    res += f"║ ❌ {title:<{width - 4}}║\n"
    res += f"╠{'═' * width}╣\n"

    # Wrapped Content
    for raw_line in text.splitlines():
        wrapped_lines = textwrap.wrap(raw_line, width - 2) or [""]
        for line in wrapped_lines:
            res += f"║ {line:<{width - 2}} ║\n"

    res += f"╚{'═' * width}╝{RESET}"
    return res


def warning_box(title: str, text: str) -> str:
    """Returns a yellow bordered box with a header and auto-wrapped message text."""
    width = DEFAULT_WIDTH

    # Header
    res = f"\n{YELLOW}┌{'─' * width}┐\n"
    res += f"│ ⚠️  {BOLD}{title:<{width - 4}}{RESET}{YELLOW}│\n"
    res += f"├{'─' * width}┤\n"

    # Wrapped Content
    for raw_line in text.splitlines():
        wrapped_lines = textwrap.wrap(raw_line, width - 2) or [""]
        for line in wrapped_lines:
            res += f"║ {line:<{width - 2}} ║\n"

    res += f"└{'─' * width}┘{RESET}"
    return res


def valid_box(title: str, text: str) -> str:
    """Returns a green bordered box with a header and auto-wrapped message text."""
    width = DEFAULT_WIDTH

    # Header
    res = f"\n{BOLD}{GREEN}╔{'═' * width}╗\n"
    res += f"║ ✅ {title:<{width - 4}}║\n"
    res += f"╠{'═' * width}╣\n"

    # Wrapped Content
    for raw_line in text.splitlines():
        wrapped_lines = textwrap.wrap(raw_line, width - 2) or [""]
        for line in wrapped_lines:
            res += f"║ {line:<{width - 2}} ║\n"

    res += f"╚{'═' * width}╝{RESET}"
    return res


# ========
# Sections
# ========
def section(step: str, name: str) -> str:
    """Numbered step section header with centered text."""
    text = f"STEP {step} — {name}"

    width = _box_width(name, 60)

    return (
        f"\n{BOLD}{PURPLE}"
        f"┌{'─' * width}┐\n"
        f"│{text:^{width}}│\n"
        f"└{'─' * width}┘"
        f"{RESET}\n"
    )


def subsection(text: str) -> str:
    """Returns a flush-left sub-header with a leading arrow and dotted underline."""
    width = len(text) + 2
    return f"\n{BOLD}{PURPLE}▸ {text}\n{'·' * width}{RESET}\n"


# =======
# Headers
# =======
def title(text: str) -> str:
    """Clean section title with subtle emphasis."""
    width = _box_width(text, 60)
    bar = "━" * width

    centered = text.center(width)

    return f"\n{BOLD}{DARK_PINK}{bar}\n" f"{centered}\n" f"{bar}{RESET}\n"


# ==================
# Lists & Key-Value
# ==================
def field(key: str, value: Any, indent: int = 2, key_width: int = 18) -> str:
    """Returns an indented, aligned key-value pair for clear data logging."""
    return f"{' ' * indent}{BOLD}{key:<{key_width}}{RESET} : {value}"


def item(text: str, indent: int = 2) -> str:
    """Indented list item."""
    return f"{' ' * indent}{text}"


# ========
# Commands
# ========
def command(cmd: list[str]) -> str:
    """
    Returns a shell-quoted, copy-pasteable representation of an argv list
    (e.g. one built for subprocess.run). Each
    part is quoted with shlex so paths containing spaces or special
    characters are shown accurately.
    """
    return " ".join(shlex.quote(part) for part in cmd)


# ========
# Messages
# ========
def ok(msg: str) -> str:
    """Success message"""
    return f"{GREEN}{OK} {msg}{RESET}\n"


def info(msg: str) -> str:
    """Neutral informational message."""
    return f"{CYAN}{INFO} {msg}{RESET}\n"


def warn(msg: str) -> str:
    """Warning message (Kept from console utils)."""
    return f"{YELLOW}{WARN} {msg}{RESET}\n"


def error(msg: str) -> str:
    """Error message (Kept from console utils)."""
    return f"{BOLD}{RED}{ERR} {msg}{RESET}\n"


def fail(msg: str) -> str:
    """Fatal failure message."""
    return f"{BOLD}{RED}{ERR} FATAL: {msg}{RESET}\n"
