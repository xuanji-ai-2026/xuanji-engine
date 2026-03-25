"""
Dialog Manage Module
Author: 雷贪音 (Employee ID: 144)
Group: XJ-09 贪狼星
Task: 对话管理实现
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time


class DialogState(Enum):
    """Dialog states."""
    IDLE = "idle"
    ACTIVE = "active"
    WAITING = "waiting"
    COMPLETED = "completed"


@dataclass
class Message:
    """Message data class."""
    message_id: str
    role: str  # user/assistant
    content: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class Dialog:
    """Dialog data class."""
    dialog_id: str
    user_id: str
    state: DialogState
    messages: List[Message] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


class DialogManager:
    """Dialog Manager Implementation"""
    
    def __init__(self):
        """Initialize the dialog manager."""
        self.dialogs: Dict[str, Dialog] = {}
        
    def create_dialog(self, dialog_id: str, user_id: str) -> Dialog:
        """Create a new dialog."""
        dialog = Dialog(
            dialog_id=dialog_id,
            user_id=user_id,
            state=DialogState.ACTIVE
        )
        
        self.dialogs[dialog_id] = dialog
        return dialog
        
    def add_message(self, dialog_id: str, role: str, content: str) -> Message:
        """Add a message to dialog."""
        if dialog_id not in self.dialogs:
            return None
            
        message = Message(
            message_id=f"{dialog_id}-{len(self.dialogs[dialog_id].messages)}",
            role=role,
            content=content
        )
        
        self.dialogs[dialog_id].messages.append(message)
        return message
        
    def get_dialog(self, dialog_id: str) -> Optional[Dialog]:
        """Get dialog by ID."""
        return self.dialogs.get(dialog_id)
        
    def get_history(self, dialog_id: str, limit: int = 10) -> List[Message]:
        """Get dialog history."""
        if dialog_id not in self.dialogs:
            return []
            
        messages = self.dialogs[dialog_id].messages
        return messages[-limit:] if limit > 0 else messages
        
    def close_dialog(self, dialog_id: str) -> bool:
        """Close a dialog."""
        if dialog_id in self.dialogs:
            self.dialogs[dialog_id].state = DialogState.COMPLETED
            return True
        return False
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "dialogs_count": len(self.dialogs),
            "active_dialogs": sum(1 for d in self.dialogs.values() if d.state == DialogState.ACTIVE)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "DialogManager",
            "version": "1.0.0",
            "status": "ready"
        }
