import { defineStore } from 'pinia'
type SceneType = 'start' | 'intro' | 'world' | 'quiz' | 'morse'| 'safe'|'ask'|'pas';
type VideoType = 'intro' | 'intro2' | 'world' | 'quiz' | 'stinger' | 'credits' | '';
export const useGameStore = defineStore('game', {
  state: () => ({
    currentScene: 'start' as SceneType,
    currentVideo: 'intro2' as VideoType,
    nextScene: 'world' as SceneType,
    nextVideo: '' as VideoType,
    focusedNpc: '' as string,
  }),
  actions: {
    goTo(scene: SceneType) {
      this.currentScene = scene
    },
    unfocusNpc() {
      this.focusedNpc = ''
    },
  }
})