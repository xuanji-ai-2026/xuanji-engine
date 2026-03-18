"""
API Route Module
Author: 康辅星 (Employee ID: 162)
Group: XJ-10 辅弼星辰
Task: API路由实现
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import re


class HTTPMethod(Enum):
    """HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Route:
    """Route data class."""
    path: str
    method: HTTPMethod
    handler: Callable
    middleware: List[Callable] = None


class APIRouter:
    """API Router Implementation"""
    
    def __init__(self):
        """Initialize the API router."""
        self.routes: List[Route] = []
        self.middleware: List[Callable] = []
        
    def add_route(
        self,
        path: str,
        method: HTTPMethod,
        handler: Callable,
        middleware: Optional[List[Callable]] = None
    ) -> None:
        """Add a route."""
        route = Route(
            path=path,
            method=method,
            handler=handler,
            middleware=middleware or []
        )
        self.routes.append(route)
        
    def get(self, path: str, handler: Callable, middleware: Optional[List[Callable]] = None) -> None:
        """Add GET route."""
        self.add_route(path, HTTPMethod.GET, handler, middleware)
        
    def post(self, path: str, handler: Callable, middleware: Optional[List[Callable]] = None) -> None:
        """Add POST route."""
        self.add_route(path, HTTPMethod.POST, handler, middleware)
        
    def put(self, path: str, handler: Callable, middleware: Optional[List[Callable]] = None) -> None:
        """Add PUT route."""
        self.add_route(path, HTTPMethod.PUT, handler, middleware)
        
    def delete(self, path: str, handler: Callable, middleware: Optional[List[Callable]] = None) -> None:
        """Add DELETE route."""
        self.add_route(path, HTTPMethod.DELETE, handler, middleware)
        
    def match_route(self, path: str, method: str) -> Optional[Route]:
        """Match a route."""
        for route in self.routes:
            if route.method.value == method:
                # Simple path matching
                if route.path == path or re.match(route.path, path):
                    return route
        return None
        
    def register_middleware(self, middleware: Callable) -> None:
        """Register global middleware."""
        self.middleware.append(middleware)
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "routes_count": len(self.routes),
            "middleware_count": len(self.middleware)
        }
        
    def get_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "APIRouter",
            "version": "1.0.0",
            "status": "ready"
        }
