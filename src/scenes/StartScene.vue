<template>
  <div class="scene start-scene">
    <video autoplay muted loop class="background-image">
      <source src="/assets/backgrounds/flag.mp4" type="video/mp4" />
    </video>
    <audio ref="audioRef" autoplay loop>
      <source src="/assets/sounds/starter.mp3" type="audio/mpeg" />
    </audio>
    <!-- <ParticleBackground :types="['dots']"/> -->
    <TransitionEffect v-if="showTransition" :effect="transitionType" @end="completeTransition" />
    <StartButton v-show="!loading" @click="start" />
    <div v-if="loading" class="loading-overlay" @click="dismissLoading">
      <div class="loading-content">
        <p>资源加载中，请稍候...</p>
        <div class="progress-bar">
          <div class="progress" :style="{ width: progressPercent + '%' }"></div>
        </div>
        <p>{{ progressPercent }}%</p>
        <p v-if="allLoaded">点击任意位置开始</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed} from 'vue'
import { useGameStore } from '../stores/game'
import StartButton from '../components/StartButton.vue'
import ParticleBackground from '../components/ParticleBackground.vue'
import TransitionEffect from '../components/TransitionEffect.vue'

const game = useGameStore()
const showTransition = ref(false)
const transitionType = ref<'zoom' | 'swirl' | 'bubble'>('zoom')
const audioRef = ref<HTMLAudioElement | null>(null)

const loading = ref(true)
const allLoaded = ref(false)
const loadedCount = ref(0)

const assetsToPreload = [
  '/assets/characters/chen_duxiu.png',
  '/assets/characters/zhang_guotao.png',
  '/assets/characters/li_da.png',
  '/assets/characters/yang_mingzhai.png',
  '/assets/characters/luo_zhanglong.png',
  '/assets/characters/wang_jinmei.png',
  '/assets/characters/xu_baihao.png',
  '/assets/characters/cai_hesen.png',
  '/assets/characters/tan_pingshan.png',
  '/assets/characters/li_zhenying.png',
  '/assets/characters/shi_cuntong.png',
  '/assets/characters/teacher_ask.png',
  '/assets/characters/teacher_cong.png',
  '/assets/characters/teacher_disap.png',
  '/assets/sounds/starter.mp3',
  '/assets/sounds/main1.mp3',
  '/assets/sounds/correct.mp3',
  '/assets/sounds/wrong.mp3',
  '/assets/backgrounds/flag.mp4',
  '/assets/backgrounds/intro.mp4',
  '/assets/backgrounds/intro2.mp4',
  '/assets/backgrounds/stinger.mp4',
  '/assets/backgrounds/credits.mp4',
  '/assets/backgrounds/history-scene.jpg',
  '/assets/backgrounds/quiz-scene.png',
  '/assets/effects/brush-stroke.png',
  '/assets/effects/confetti.gif',
  // '/assets/text/questions.jsonl',
]

const progressPercent = computed(() => {
  return Math.floor((loadedCount.value / assetsToPreload.length) * 100)
})

function preloadAssets() {
  function onAssetLoad() {
    loadedCount.value++
    if (loadedCount.value === assetsToPreload.length) {
      allLoaded.value = true
    }
  }

  assetsToPreload.forEach(src => {
    if (src.endsWith('.mp3')) {
      const audio = new Audio()
      audio.oncanplaythrough = onAssetLoad
      audio.src = src
    } else if (src.endsWith('.mp4')) {
      const video = document.createElement('video')
      video.oncanplaythrough = onAssetLoad
      video.src = src
      video.load()
    } else {
      const img = new Image()
      img.onload = onAssetLoad
      img.src = src
    }
  })
}

// const allAssets = import.meta.glob(
//   [
//     '/assets/**/*.png',
//     '/assets/**/*.jpg',
//     '/assets/**/*.jpeg',
//     '/assets/**/*.mp3',
//     '/assets/**/*.mp4',
//     '/assets/**/*.webp'
//   ],
//   { eager: true, as: 'url' }
// )

// const totalCount = Object.keys(allAssets).length

// const progressPercent = computed(() =>
//   Math.floor((loadedCount.value / totalCount) * 100)
// )

// function preloadAssets() {
//   Object.values(allAssets).forEach(src => {
//     let element: HTMLImageElement | HTMLVideoElement | HTMLAudioElement

//     if (src.endsWith('.mp3')) {
//       element = new Audio()
//       element.oncanplaythrough = onAssetLoaded
//     } else if (src.endsWith('.mp4')) {
//       element = document.createElement('video')
//       element.oncanplaythrough = onAssetLoaded
//     } else {
//       element = new Image()
//       element.onload = onAssetLoaded
//     }

//     element.src = src
//   })
// }

// function onAssetLoaded() {
//   loadedCount.value++
//   if (loadedCount.value >= totalCount) {
//     allLoaded.value = true
//   }
// }

function dismissLoading() {
  if (allLoaded.value) loading.value = false
}

onMounted(() => {
  preloadAssets()

  if (audioRef.value) {
    // 尝试直接播放
    audioRef.value.play().then(() => {
      console.log('背景音乐自动播放成功')
    }).catch((err) => {
      console.warn('背景音乐自动播放被阻止，等待用户交互触发')
      // 如果自动播放失败，需要用户点击后再播放
      const resumeAudio = () => {
        audioRef.value?.play()
        window.removeEventListener('click', resumeAudio)
        window.removeEventListener('touchstart', resumeAudio)
      }
      window.addEventListener('click', resumeAudio)
      window.addEventListener('touchstart', resumeAudio)
    })
  }
})

function start() {
  // showTransition.value = true
  completeTransition()
}

function completeTransition() {
  game.currentVideo = 'intro'
  game.nextScene = 'world'
  game.goTo('intro')
}
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

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: white;
  font-size: 1.5rem;
  z-index: 10;
}

.progress-bar {
  width: 300px;
  height: 20px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  margin: 1rem 0;
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: white;
  transition: width 0.3s ease;
}

.spinner {
  margin: 1rem;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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