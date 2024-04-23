from enum import Enum


class Choice(Enum):
    STARTED = "started"
    RESTARTED = "restarted"
    STOPPED = "stopped"
    ENABLED = "enabled"
    DISABLED = "disabled"
    PRESENT = "present"
    ABSENT = "absent"
