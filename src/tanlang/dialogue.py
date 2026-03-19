"""
贪狼星 - 对话API模块
ASR/TTS、2D数字人、交互层
"""

import asyncio
import base64
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageRole(str, Enum):
    """消息角色"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """对话消息"""
    role: MessageRole
    content: str
    timestamp: float = Field(default_factory=lambda: asyncio.get_event_loop().time())


class DialogueSession(BaseModel):
    """对话会话"""
    session_id: str
    user_id: str
    messages: List[Message] = Field(default_factory=list)
    context: Dict = Field(default_factory=dict)
    created_at: float = Field(default_factory=lambda: asyncio.get_event_loop().time())


class TTSRequest(BaseModel):
    """TTS请求"""
    text: str
    voice: str = Field(default="default")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


class ASRRequest(BaseModel):
    """ASR请求"""
    audio_data: str  # base64编码


class DialogueEngine:
    """对话引擎"""
    
    def __init__(self):
        self.sessions: Dict[str, DialogueSession] = {}
        self.default_system_prompt = """你是一个专业的AI助手，名叫玄玑。
请用友好、专业的方式回答用户的问题。"""
    
    def create_session(self, session_id: str, user_id: str) -> DialogueSession:
        """创建会话"""
        session = DialogueSession(
            session_id=session_id,
            user_id=user_id,
            messages=[
                Message(role=MessageRole.SYSTEM, content=self.default_system_prompt)
            ]
        )
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[DialogueSession]:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def add_message(
        self,
        session_id: str,
        role: MessageRole,
        content: str
    ) -> bool:
        """添加消息"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        session.messages.append(Message(role=role, content=content))
        return True
    
    def get_history(
        self,
        session_id: str,
        limit: int = 10
    ) -> List[Message]:
        """获取历史消息"""
        session = self.sessions.get(session_id)
        if not session:
            return []
        
        return session.messages[-limit:]
    
    def clear_session(self, session_id: str) -> bool:
        """清除会话"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


class TTSEngine(BaseModel):
    """TTS语音合成引擎"""
    
    default_voice: str = "default"
    
    async def synthesize(self, request: TTSRequest) -> Dict:
        """合成语音"""
        # 模拟TTS
        return {
            "status": "success",
            "audio_base64": "mock_audio_data",
            "format": "mp3",
            "duration": len(request.text) * 0.1
        }
    
    def list_voices(self) -> List[Dict]:
        """列出可用音色"""
        return [
            {"id": "default", "name": "默认女声"},
            {"id": "male", "name": "男声"},
            {"id": "female_young", "name": "年轻女声"},
            {"id": "male_senior", "name": "中年男声"}
        ]


class ASREngine(BaseModel):
    """ASR语音识别引擎"""
    
    async def recognize(self, request: ASRRequest) -> Dict:
        """识别语音"""
        # 模拟ASR
        return {
            "status": "success",
            "text": "这是识别到的文本",
            "confidence": 0.95,
            "language": "zh-CN"
        }
    
    def list_languages(self) -> List[str]:
        """列出支持的语言"""
        return ["zh-CN", "en-US", "vi-VN", "ja-JP"]


class DigitalPersona(BaseModel):
    """数字人"""
    name: str
    avatar: str = ""
    voice: str = "default"
    animation: str = "idle"
    
    class Config:
        arbitrary_types_allowed = True


class DialogueManager:
    """对话管理器 - 管理多个对话会话和流程"""
    
    def __init__(self):
        self.dialogue_engine = DialogueEngine()
        self.tts_engine = TTSEngine()
        self.asr_engine = ASREngine()
        self.persona_manager = DigitalPersonaManager()
        self.active_dialogues: Dict[str, Dict] = {}
    
    async def start_dialogue(
        self,
        session_id: str,
        user_id: str,
        persona_id: str = "default"
    ) -> Dict:
        """开始对话"""
        # 创建会话
        session = self.dialogue_engine.create_session(session_id, user_id)
        
        # 获取数字人
        persona = self.persona_manager.get_persona(persona_id)
        
        # 记录活跃对话
        self.active_dialogues[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "persona_id": persona_id,
            "persona": persona,
            "start_time": asyncio.get_event_loop().time(),
            "message_count": 1
        }
        
        return {
            "session_id": session_id,
            "persona": persona.dict() if persona else None,
            "status": "started"
        }
    
    async def send_message(
        self,
        session_id: str,
        message: str,
        role: str = "user"
    ) -> Dict:
        """发送消息"""
        # 添加消息到会话
        success = self.dialogue_engine.add_message(
            session_id,
            MessageRole.USER if role == "user" else MessageRole.ASSISTANT,
            message
        )
        
        if not success:
            return {"status": "error", "message": "Session not found"}
        
        # 更新对话统计
        if session_id in self.active_dialogues:
            self.active_dialogues[session_id]["message_count"] += 1
        
        # 获取对话历史
        history = self.dialogue_engine.get_history(session_id)
        
        # 模拟AI响应（实际接入DeepSeek）
        response = self._generate_response(history)
        
        # 添加AI回复
        self.dialogue_engine.add_message(
            session_id,
            MessageRole.ASSISTANT,
            response
        )
        
        return {
            "status": "success",
            "response": response,
            "message_count": len(history)
        }
    
    async def send_audio_message(
        self,
        session_id: str,
        audio_data: str
    ) -> Dict:
        """发送语音消息（ASR + 对话 + TTS）"""
        # 语音识别
        asr_result = await self.asr_engine.recognize(
            ASRRequest(audio_data=audio_data)
        )
        
        if asr_result.confidence < 0.7:
            return {
                "status": "error",
                "message": "语音识别置信度低",
                "confidence": asr_result.confidence
            }
        
        # 文本对话
        dialogue_result = await self.send_message(
            session_id,
            asr_result.text
        )
        
        # 语音合成
        tts_result = await self.tts_engine.synthesize(
            TTSRequest(text=dialogue_result["response"])
        )
        
        return {
            "status": "success",
            "recognized_text": asr_result.text,
            "confidence": asr_result.confidence,
            "response": dialogue_result["response"],
            "audio_base64": tts_result.audio_base64,
            "audio_format": tts_result.format,
            "duration": tts_result.duration
        }
    
    def get_dialogue_state(self, session_id: str) -> Dict:
        """获取对话状态"""
        session = self.active_dialogues.get(session_id)
        if not session:
            return {"status": "error", "message": "Dialogue not found"}
        
        history = self.dialogue_engine.get_history(session_id)
        
        return {
            "status": "success",
            "session_id": session_id,
            "persona": session["persona"].dict() if session.get("persona") else None,
            "message_count": session["message_count"],
            "duration": asyncio.get_event_loop().time() - session["start_time"]
        }
    
    async def end_dialogue(self, session_id: str) -> bool:
        """结束对话"""
        success = self.dialogue_engine.clear_session(session_id)
        if session_id in self.active_dialogues:
            del self.active_dialogues[session_id]
        return success
    
    def _generate_response(self, history: List[Message]) -> str:
        """生成AI响应"""
        # 这里接入DeepSeek API进行实际对话
        # 当前返回模拟响应
        return "这是AI的回复。实际开发中将接入DeepSeek API。"


class DigitalPersonaManager:
    """数字人管理器"""
    
    def __init__(self):
        self.personas: Dict[str, DigitalPersona] = {}
        self._init_default_personas()
    
    def _init_default_personas(self):
        """初始化默认数字人"""
        self.personas["default"] = DigitalPersona(
            name="小玑",
            avatar="/avatars/xiaoqi.png",
            voice="female_young",
            animation="idle"
        )
        
        self.personas["professional"] = DigitalPersona(
            name="专业助手",
            avatar="/avatars/pro.png",
            voice="male",
            animation="professional"
        )
    
    def get_persona(self, persona_id: str) -> Optional[DigitalPersona]:
        """获取数字人"""
        return self.personas.get(persona_id)
    
    def list_personas(self) -> List[DigitalPersona]:
        """列出所有数字人"""
        return list(self.personas.values())


# 测试代码
if __name__ == "__main__":
    async def test():
        # 对话引擎测试
        dialogue = DialogueEngine()
        session = dialogue.create_session("sess_001", "user_001")
        dialogue.add_message("sess_001", MessageRole.USER, "你好")
        
        history = dialogue.get_history("sess_001")
        print("对话历史:", len(history))
        
        # TTS测试
        tts = TTSEngine()
        result = await tts.synthesize(TTSRequest(text="你好"))
        print("TTS结果:", result)
        
        # ASR测试
        asr = ASREngine()
        result = await asr.recognize(ASRRequest(audio_data="mock"))
        print("ASR结果:", result)
    
    asyncio.run(test())
