/**
 * 小紫 - 用户端智能助手适配层
 * 主入口文件
 */

export { XiaopurpleAdapter } from './XiaopurpleAdapter';
export { GuideEngine } from './GuideEngine';
export { RecommendationEngine } from './RecommendationEngine';
export { DiagnosticEngine } from './DiagnosticEngine';
export { AutomationEngine } from './AutomationEngine';

export type {
  // 基础类型
  MessageType,
  MessageRole,
  ConnectionState,

  // 消息类型
  BaseMessage,
  TextMessage,
  VoiceMessage,
  ImageMessage,
  SystemMessage,
  Message,

  // 对话会话
  Conversation,

  // 智能引导
  GuideType,
  GuideStep,
  GuideAction,
  GuideFlow,
  GuideState,

  // 推荐引擎
  UserBehavior,
  Recommendation,
  RecommendationAction,
  RecommendationType,
  UserProfile,

  // 问题诊断
  DiagnosticResult,
  Solution,

  // 自动化操作
  AutomationTask,
  AutomationStep,

  // 配置和事件
  XiaopurpleConfig,
  AdapterEvent,
  EventHandler,
  ApiResponse,
  StreamResponse,
  WSMessage
} from '../types';
