"""
Support System Module
Author: 桥客服 (Employee ID: 188)
Group: XJ-10 辅弼星辰
Task: 客服系统实现
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import time


class TicketStatus(Enum):
    """Ticket status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(Enum):
    """Ticket priority."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Ticket:
    """Support ticket data class."""
    ticket_id: str
    user_id: str
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: float = field(default_factory=time.time)
    resolved_at: float = None


class SupportSystem:
    """Support System Implementation"""
    
    def __init__(self):
        """Initialize the support system."""
        self.tickets: Dict[str, Ticket] = {}
        self.assignments: Dict[str, str] = {}  # ticket_id -> agent_id
        
    def create_ticket(
        self,
        ticket_id: str,
        user_id: str,
        subject: str,
        description: str,
        priority: TicketPriority = TicketPriority.NORMAL
    ) -> Ticket:
        """Create a new support ticket."""
        ticket = Ticket(
            ticket_id=ticket_id,
            user_id=user_id,
            subject=subject,
            description=description,
            status=TicketStatus.OPEN,
            priority=priority
        )
        
        self.tickets[ticket_id] = ticket
        return ticket
        
    def assign_ticket(self, ticket_id: str, agent_id: str) -> bool:
        """Assign ticket to an agent."""
        if ticket_id in self.tickets:
            self.assignments[ticket_id] = agent_id
            self.tickets[ticket_id].status = TicketStatus.IN_PROGRESS
            return True
        return False
        
    def resolve_ticket(self, ticket_id: str) -> bool:
        """Resolve a ticket."""
        if ticket_id in self.tickets:
            self.tickets[ticket_id].status = TicketStatus.RESOLVED
            self.tickets[ticket_id].resolved_at = time.time()
            return True
        return False
        
    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID."""
        return self.tickets.get(ticket_id)
        
    def get_user_tickets(self, user_id: str) -> List[Ticket]:
        """Get all tickets for a user."""
        return [t for t in self.tickets.values() if t.user_id == user_id]
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "tickets_count": len(self.tickets),
            "open_tickets": sum(1 for t in self.tickets.values() if t.status == TicketStatus.OPEN),
            "resolved_tickets": sum(1 for t in self.tickets.values() if t.status == TicketStatus.RESOLVED)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "SupportSystem",
            "version": "1.0.0",
            "status": "ready"
        }
