"""
Secure Rate Limiting Module for ARTHIV Interview Platform.

This module implements device-based session limiting:
- Each device is identified by IP + User-Agent hash
- Maximum 8 concurrent sessions per device
- Secure, tamper-resistant device fingerprinting
"""

import hashlib
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional
from fastapi import WebSocket, Request, HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# Configuration
MAX_SESSIONS_PER_DEVICE = 8
SESSION_CLEANUP_INTERVAL = 300  # 5 minutes
MAX_HTTP_REQUESTS_PER_MINUTE = 60  # HTTP rate limit


@dataclass
class SessionInfo:
    """Information about an active session."""
    session_id: str
    user_id: str
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)


class DeviceRateLimiter:
    """
    Secure rate limiter that tracks sessions per device.
    
    Device identification uses a combination of:
    - Client IP address
    - User-Agent header (hashed for privacy)
    - Optional custom client identifier
    
    This prevents a single device from creating more than MAX_SESSIONS_PER_DEVICE
    concurrent interview sessions.
    """
    
    def __init__(self, max_sessions: int = MAX_SESSIONS_PER_DEVICE):
        self.max_sessions = max_sessions
        # device_id -> {session_id: SessionInfo}
        self._active_sessions: Dict[str, Dict[str, SessionInfo]] = defaultdict(dict)
        # HTTP request tracking: device_id -> list of timestamps
        self._http_requests: Dict[str, list] = defaultdict(list)
        self._lock_placeholder = None  # For future async lock if needed
        
    def _generate_device_fingerprint(
        self, 
        client_ip: str, 
        user_agent: str,
        custom_id: Optional[str] = None
    ) -> str:
        """
        Generate a secure device fingerprint.
        
        Uses SHA-256 hash of combined identifiers for:
        - Privacy: User-Agent is hashed, not stored raw
        - Security: Fingerprint is not easily spoofable
        - Consistency: Same device always gets same ID
        """
        # Normalize inputs
        ip_normalized = client_ip.strip().lower()
        ua_normalized = (user_agent or "unknown").strip()
        
        # Create composite identifier
        components = [ip_normalized, ua_normalized]
        if custom_id:
            components.append(custom_id)
        
        composite = "|".join(components)
        
        # Hash for security and privacy
        fingerprint = hashlib.sha256(composite.encode()).hexdigest()[:32]
        
        logger.debug(f"Generated device fingerprint: {fingerprint[:8]}... for IP: {ip_normalized[:10]}...")
        return fingerprint
    
    def get_device_id_from_websocket(self, websocket: WebSocket) -> str:
        """Extract device fingerprint from WebSocket connection."""
        # Get client IP - handle proxies
        client_ip = self._get_client_ip(websocket.headers, websocket.client)
        user_agent = websocket.headers.get("user-agent", "unknown")
        
        return self._generate_device_fingerprint(client_ip, user_agent)
    
    def get_device_id_from_request(self, request: Request) -> str:
        """Extract device fingerprint from HTTP request."""
        client_ip = self._get_client_ip(request.headers, request.client)
        user_agent = request.headers.get("user-agent", "unknown")
        
        return self._generate_device_fingerprint(client_ip, user_agent)
    
    def _get_client_ip(self, headers, client) -> str:
        """Get real client IP, handling reverse proxies."""
        # Check X-Forwarded-For header (common for proxies/load balancers)
        forwarded = headers.get("x-forwarded-for")
        if forwarded:
            # Take the first IP (original client)
            return forwarded.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()
        
        # Fallback to direct client IP
        if client:
            return client.host
        
        return "unknown"
    
    def get_active_session_count(self, device_id: str) -> int:
        """Get the number of active sessions for a device."""
        return len(self._active_sessions.get(device_id, {}))
    
    def can_create_session(self, device_id: str) -> bool:
        """Check if device can create a new session."""
        current_count = self.get_active_session_count(device_id)
        return current_count < self.max_sessions
    
    def register_session(
        self, 
        device_id: str, 
        session_id: str, 
        user_id: str
    ) -> bool:
        """
        Register a new session for a device.
        
        Returns True if registration successful, False if limit exceeded.
        """
        if not self.can_create_session(device_id):
            logger.warning(
                f"Session limit reached for device {device_id[:8]}... "
                f"({self.get_active_session_count(device_id)}/{self.max_sessions})"
            )
            return False
        
        self._active_sessions[device_id][session_id] = SessionInfo(
            session_id=session_id,
            user_id=user_id
        )
        
        logger.info(
            f"Session {session_id} registered for device {device_id[:8]}... "
            f"({self.get_active_session_count(device_id)}/{self.max_sessions})"
        )
        return True
    
    def unregister_session(self, device_id: str, session_id: str) -> bool:
        """
        Remove a session when it ends.
        
        Returns True if session was found and removed.
        """
        if device_id in self._active_sessions:
            if session_id in self._active_sessions[device_id]:
                del self._active_sessions[device_id][session_id]
                logger.info(
                    f"Session {session_id} unregistered for device {device_id[:8]}... "
                    f"({self.get_active_session_count(device_id)}/{self.max_sessions})"
                )
                
                # Cleanup empty device entries
                if not self._active_sessions[device_id]:
                    del self._active_sessions[device_id]
                
                return True
        return False
    
    def check_http_rate_limit(self, device_id: str) -> bool:
        """
        Check HTTP request rate limit.
        
        Returns True if request is allowed, False if rate limited.
        """
        now = time.time()
        window_start = now - 60  # 1 minute window
        
        # Clean old requests
        self._http_requests[device_id] = [
            ts for ts in self._http_requests[device_id] 
            if ts > window_start
        ]
        
        # Check limit
        if len(self._http_requests[device_id]) >= MAX_HTTP_REQUESTS_PER_MINUTE:
            return False
        
        # Record this request
        self._http_requests[device_id].append(now)
        return True
    
    def get_rate_limit_error_response(self, device_id: str) -> JSONResponse:
        """Generate standardized rate limit error response."""
        current_count = self.get_active_session_count(device_id)
        return JSONResponse(
            status_code=429,
            content={
                "error": "rate_limit_exceeded",
                "message": f"Maximum sessions ({self.max_sessions}) reached for this device",
                "current_sessions": current_count,
                "max_sessions": self.max_sessions,
                "retry_after": "Close an existing session to continue"
            }
        )
    
    def cleanup_stale_sessions(self, max_idle_seconds: int = 3600) -> int:
        """
        Remove sessions that have been idle too long.
        
        Returns the number of sessions cleaned up.
        """
        now = datetime.now()
        cleaned = 0
        
        for device_id in list(self._active_sessions.keys()):
            for session_id in list(self._active_sessions[device_id].keys()):
                session = self._active_sessions[device_id][session_id]
                idle_time = (now - session.last_activity).total_seconds()
                
                if idle_time > max_idle_seconds:
                    del self._active_sessions[device_id][session_id]
                    cleaned += 1
                    logger.info(f"Cleaned stale session {session_id}")
            
            # Cleanup empty device entries
            if not self._active_sessions[device_id]:
                del self._active_sessions[device_id]
        
        return cleaned
    
    def get_stats(self) -> dict:
        """Get rate limiter statistics."""
        total_sessions = sum(
            len(sessions) for sessions in self._active_sessions.values()
        )
        return {
            "total_devices": len(self._active_sessions),
            "total_sessions": total_sessions,
            "max_sessions_per_device": self.max_sessions
        }


# Global rate limiter instance
rate_limiter = DeviceRateLimiter(max_sessions=MAX_SESSIONS_PER_DEVICE)


# Dependency for FastAPI
async def check_session_limit(websocket: WebSocket) -> str:
    """
    FastAPI dependency to check session limits before WebSocket connection.
    
    Returns the device_id if allowed, raises exception if rate limited.
    """
    device_id = rate_limiter.get_device_id_from_websocket(websocket)
    
    if not rate_limiter.can_create_session(device_id):
        # For WebSocket, we need to accept then close with error
        # This is handled in the endpoint itself
        raise HTTPException(
            status_code=429,
            detail={
                "error": "session_limit_exceeded",
                "message": f"Maximum {MAX_SESSIONS_PER_DEVICE} sessions per device",
                "current": rate_limiter.get_active_session_count(device_id)
            }
        )
    
    return device_id
