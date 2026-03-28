import { create } from 'zustand';
import type { DigitalHuman, DigitalHumanTemplate } from '@/types';
import digitalHumanService from '@/services/digital-human';

interface DigitalHumanState {
  digitalHumans: DigitalHuman[];
  templates: DigitalHumanTemplate[];
  selectedDigitalHuman: DigitalHuman | null;
  isLoading: boolean;
  error: string | null;
  totalCount: number;
  currentPage: number;

  fetchDigitalHumans: (page?: number) => Promise<void>;
  fetchTemplates: () => Promise<void>;
  createDigitalHuman: (data: any) => Promise<DigitalHuman>;
  updateDigitalHuman: (id: string, data: any) => Promise<void>;
  deleteDigitalHuman: (id: string) => Promise<void>;
  selectDigitalHuman: (digitalHuman: DigitalHuman | null) => void;
  startDigitalHuman: (id: string) => Promise<void>;
  stopDigitalHuman: (id: string) => Promise<void>;
  cloneDigitalHuman: (id: string, name: string) => Promise<void>;
  clearError: () => void;
}

export const useDigitalHumanStore = create<DigitalHumanState>((set, _get) => ({
  digitalHumans: [],
  templates: [],
  selectedDigitalHuman: null,
  isLoading: false,
  error: null,
  totalCount: 0,
  currentPage: 1,

  fetchDigitalHumans: async (page = 1) => {
    set({ isLoading: true, error: null });
    try {
      const response = await digitalHumanService.getDigitalHumanList({
        page,
        pageSize: 20,
      });
      set({
        digitalHumans: response.items,
        totalCount: response.total,
        currentPage: page,
        isLoading: false,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '获取数字人列表失败',
      });
      throw error;
    }
  },

  fetchTemplates: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await digitalHumanService.getTemplateList({
        page: 1,
        pageSize: 50,
      });
      set({
        templates: response.items,
        isLoading: false,
      });
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '获取模板列表失败',
      });
      throw error;
    }
  },

  createDigitalHuman: async (data) => {
    set({ isLoading: true, error: null });
    try {
      const newDigitalHuman = await digitalHumanService.createDigitalHuman(data);
      set((state) => ({
        digitalHumans: [newDigitalHuman, ...state.digitalHumans],
        totalCount: state.totalCount + 1,
        isLoading: false,
      }));
      return newDigitalHuman;
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '创建数字人失败',
      });
      throw error;
    }
  },

  updateDigitalHuman: async (id, data) => {
    set({ isLoading: true, error: null });
    try {
      const updatedDigitalHuman = await digitalHumanService.updateDigitalHuman(
        id,
        data
      );
      set((state) => ({
        digitalHumans: state.digitalHumans.map((dh) =>
          dh.id === id ? updatedDigitalHuman : dh
        ),
        selectedDigitalHuman:
          state.selectedDigitalHuman?.id === id
            ? updatedDigitalHuman
            : state.selectedDigitalHuman,
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '更新数字人失败',
      });
      throw error;
    }
  },

  deleteDigitalHuman: async (id) => {
    set({ isLoading: true, error: null });
    try {
      await digitalHumanService.deleteDigitalHuman(id);
      set((state) => ({
        digitalHumans: state.digitalHumans.filter((dh) => dh.id !== id),
        totalCount: state.totalCount - 1,
        selectedDigitalHuman:
          state.selectedDigitalHuman?.id === id
            ? null
            : state.selectedDigitalHuman,
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '删除数字人失败',
      });
      throw error;
    }
  },

  selectDigitalHuman: (digitalHuman) => {
    set({ selectedDigitalHuman: digitalHuman });
  },

  startDigitalHuman: async (id) => {
    try {
      await digitalHumanService.startDigitalHuman(id);
      set((state) => ({
        digitalHumans: state.digitalHumans.map((dh) =>
          dh.id === id ? { ...dh, status: 'active' } : dh
        ),
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '启动失败',
      });
      throw error;
    }
  },

  stopDigitalHuman: async (id) => {
    try {
      await digitalHumanService.stopDigitalHuman(id);
      set((state) => ({
        digitalHumans: state.digitalHumans.map((dh) =>
          dh.id === id ? { ...dh, status: 'inactive' } : dh
        ),
      }));
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : '停止失败',
      });
      throw error;
    }
  },

  cloneDigitalHuman: async (id, name) => {
    set({ isLoading: true, error: null });
    try {
      const clonedDigitalHuman = await digitalHumanService.cloneDigitalHuman(id, name);
      set((state) => ({
        digitalHumans: [clonedDigitalHuman, ...state.digitalHumans],
        totalCount: state.totalCount + 1,
        isLoading: false,
      }));
    } catch (error) {
      set({
        isLoading: false,
        error: error instanceof Error ? error.message : '克隆失败',
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));
