"""
ASR Interface Module
Author: 贺贪形 (Employee ID: 145)
Group: XJ-09 贪狼星
Task: ASR接口实现
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import base64


class ASRStatus(Enum):
    """ASR status."""
    IDLE = "idle"
    RECORDING = "recording"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


class ASRInterface:
    """ASR Interface Implementation"""
    
    def __init__(self):
        """Initialize the ASR interface."""
        self.status = ASRStatus.IDLE
        self.results: Dict[str, str] = {}  # audio_id -> text
        self.callbacks: List[Callable] = []
        
    def start_recording(self) -> str:
        """Start audio recording."""
        self.status = ASRStatus.RECORDING
        return f"recording-{int(time.time())}"
        
    def stop_recording(self, recording_id: str) -> bool:
        """Stop audio recording."""
        if self.status == ASRStatus.RECORDING:
            self.status = ASRStatus.PROCESSING
            return True
        return False
        
    def process_audio(self, audio_data: bytes) -> str:
        """
        Process audio data and return text.
        
        Args:
            audio_data: Audio data in bytes
            
        Returns:
            Recognized text
        """
        self.status = ASRStatus.PROCESSING
        
        # Simulate ASR processing
        text = "Sample transcribed text"
        
        audio_id = f"audio-{len(self.results)}"
        self.results[audio_id] = text
        self.status = ASRStatus.COMPLETED
        
        return text
        
    def process_audio_base64(self, audio_base64: str) -> str:
        """Process base64 encoded audio."""
        try:
            audio_data = base64.b64decode(audio_base64)
            return self.process_audio(audio_data)
        except Exception:
            self.status = ASRStatus.ERROR
            return ""
            
    def get_result(self, audio_id: str) -> Optional[str]:
        """Get ASR result."""
        return self.results.get(audio_id)
        
    def register_callback(self, callback: Callable) -> None:
        """Register completion callback."""
        self.callbacks.append(callback)
        
    def get_status(self) -> Dict[str, Any]:
        """Get module status."""
        return {
            "status": self.status.value,
            "results_count": len(self.results)
        }
        
    def get_module_result(self) -> Dict[str, Any]:
        """Get module result."""
        return {
            "module": "ASRInterface",
            "version": "1.0.0",
            "status": "ready"
        }
