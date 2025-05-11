<template>
  <div class="scene intro-scene">
    <video autoplay ref ="videoRef" class="background-image" @ended="onVideoEnded">
      <source :src="backgroundVideo" type="video/mp4" />
    </video>
    <button class="skip-btn" @click="enterWorld">跳过 ></button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useGameStore } from '../stores/game'
const game = useGameStore()
const backgroundVideo = computed(() => `/assets/backgrounds/${game.currentVideo}.mp4`)
const nextScene = game.nextScene
const videoRef = ref<HTMLVideoElement | null>(null)

function enterWorld() {
  if (game.nextVideo !== '') {
    game.currentVideo = game.nextVideo
    game.nextVideo = ''
    return
  }
  else
    game.goTo(nextScene)
}

function onVideoEnded() {
  // Perform actions when the video ends
  enterWorld()
}

watch(() => game.currentVideo, () => {
  if (videoRef.value) {
    videoRef.value.load()
    videoRef.value.play().catch(() => {
      // 自动播放可能失败（浏览器策略），可忽略
    })
  }
})

</script>

<style scoped>
.scene {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  object-fit: cover;
  z-index: 0;
  pointer-events: none;
}

.skip-btn {
  float: left;
  position: absolute;
  bottom: 20px;
  right: 20px;
  z-index: 1;
  color: white;
  font-size: 20px;
  font-weight: bold;
  font-style: italic;
  background-color: transparent;
  border: none;
  cursor: pointer;
  animation: breathe 2s infinite alternate;
}
</style>

<style>
html,
body {
  margin: 0;
  padding: 0;
  overflow: hidden;
}
</style>