<template>
  <div id="app">
    <transition name="fade" mode="out-in">
      <component :is="sceneComponent" :key="currentScene" />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useGameStore } from './stores/game'
import StartScene from './scenes/StartScene.vue'
import IntroScene from './scenes/IntroScene.vue'
import WorldScene from './scenes/WorldScene.vue'
import QuizScene from './scenes/QuizScene.vue'

const { currentScene } = storeToRefs(useGameStore())

const sceneComponent = computed(() => {
  switch (currentScene.value) {
    case 'start': return StartScene
    case 'intro': return IntroScene
    case 'world': return WorldScene
    case 'quiz': return QuizScene
    default: return StartScene
  }
})
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.8s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.confetti-effect {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 600px;
  height: 600px;
  background-image: url('/assets/effects/confetti.gif'); /* ✅ 确保路径正确 */
  background-size: contain;
  background-repeat: no-repeat;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 9999;
}
</style>