from .actions import show_desktop, open_notepad, terminate_notepad
from .grounding import (
    ground_notepad_icon,
    validate_notepad_window,
    terminate_notepad_if_open,
    OS_FALLBACK_SUCCESS
)
from .writer import write_post_to_notepad
