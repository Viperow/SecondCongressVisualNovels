<template>
  <div class="scene world-scene" @mousemove="handleMouseMove">
    <div class="world-wrapper" :class="{ blurred: focused }" :style="wrapperStyle" ref="wrapper">
      <img src="/assets/backgrounds/history-scene.jpg" class="world-background" :style="backgroundStyle" />
      <div v-for="npc in npcs" :key="npc.id" v-show="npc.visible" class="npc" :style="npcStyle(npc)"
        @mouseenter="hoveredNpc = npc.id" @mouseleave="hoveredNpc = null" @click="selectNpc(npc.id)">
        <img :src="npc.img" :class="{ highlight: hoveredNpc === npc.id }" />
      </div>
    </div>
    <audio autoplay loop>
      <source src="/assets/sounds/main1.mp3" type="audio/mpeg" />
    </audio>
    <!-- 聚焦模式 -->
    <DialogueOverlay :visible="focused" :npcName="focusedNpcName" :npcImage="focusedNpcImage" :response="response"
      :loading="loading" mode="dialogue" @ask="ask" @return="clearFocus" />
    <button class="awake-btn" @click="enterQuiz">醒来 ></button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import { useGameStore } from '../stores/game'

const game = useGameStore()
const hoveredNpc = ref<string | null>(null)
const focused = ref(false)
const focusedNpc = ref<string | null>(null)
const mouseX = ref(0)
const offsetX = ref(0)
const focusedOffsetX = ref(0)
const sceneWidth = 6000 // 设计稿宽度
const sceneHeight = 1000 // 设计稿高度
const userInput = ref('')
const response = ref('')
const loading = ref(false)
const isTyping = ref(false)             // 是否正在流式输出
const dialogueContent = ref<HTMLDivElement | null>(null)
const wrapper = ref<HTMLDivElement | null>(null)
const allowMouseMove = ref(false)

let socket: WebSocket | null = null

const npcs = [
  { id: 'chen_duxiu', name: '陈独秀', x: 200, y: 800, scale: 1.2, z: 2, img: '/assets/characters/chen_duxiu.png', visible: true },
  { id: 'zhang_guotao', name: '张国焘', x: 800, y: 800, scale: 1.2, z: 2, img: '/assets/characters/zhang_guotao.png', visible: true },
  { id: 'li_da', name: '李达', x: 1400, y: 800, scale: 1.2, z: 2, img: '/assets/characters/li_da.png', visible: true },
  { id: 'yang_mingzhai', name: '杨明斋', x: 2000, y: 800, scale: 1.2, z: 2, img: '/assets/characters/yang_mingzhai.png', visible: true },
  { id: 'luo_zhanglong', name: '罗章龙', x: 2600, y: 800, scale: 1.2, z: 2, img: '/assets/characters/luo_zhanglong.png', visible: true },
  { id: 'wang_jinmei', name: '王尽美', x: 3200, y: 800, scale: 1.2, z: 2, img: '/assets/characters/wang_jinmei.png', visible: true },
  { id: 'xu_baihao', name: '许白昊', x: 600, y: 700, scale: 0.9, z: 1, img: '/assets/characters/xu_baihao.png', visible: true },
  { id: 'cai_hesen', name: '蔡和森', x: 1100, y: 700, scale: 0.9, z: 1, img: '/assets/characters/cai_hesen.png', visible: true },
  { id: 'tan_pingshan', name: '谭平山', x: 1700, y: 700, scale: 0.9, z: 1, img: '/assets/characters/tan_pingshan.png', visible: true },
  { id: 'li_zhenying', name: '李震瀛', x: 2300, y: 700, scale: 0.9, z: 1, img: '/assets/characters/li_zhenying.png', visible: true },
  { id: 'shi_cuntong', name: '施存统', x: 2900, y: 700, scale: 0.9, z: 1, img: '/assets/characters/shi_cuntong.png', visible: true }
]

const scale = ref(1)

const updateScale = () => {
  scale.value = window.innerHeight / sceneHeight
}

onMounted(() => {
  updateScale()
  window.addEventListener('resize', updateScale)
  setTimeout(() => {
    allowMouseMove.value = true
  }, 300) // 300ms 等动画结束后再启用交互
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScale)
})

function selectNpc(id: string) {
  focusedNpc.value = id
  focused.value = true
  const npc = npcs.find(n => n.id === id)
  if (npc) npc.visible = false
  focusedOffsetX.value = offsetX.value
}

function clearFocus() {
  if (focusedNpc.value) {
    const npc = npcs.find(n => n.id === focusedNpc.value)
    if (npc) npc.visible = true
  }
  focusedNpc.value = null
  focused.value = false
  response.value = ''
}

function handleMouseMove(e: MouseEvent) {
  // mouseX.value = e.clientX
  // let moveX = -(mouseX.value - window.innerWidth / 2)
  // offsetX.value = Math.max(-sceneWidth / 6.8, Math.min(Math.min(moveX, 0), sceneWidth - window.innerWidth))
  if (!allowMouseMove.value || focused.value) return
  const totalWidth = sceneWidth * 0.8 * scale.value
  const maxOffset = 0
  const minOffset = window.innerWidth - totalWidth
  let moveX = -(e.clientX / window.innerWidth - 0.5) * (totalWidth - window.innerWidth)
  offsetX.value = Math.min(maxOffset, Math.max(minOffset, moveX))
}

const wrapperStyle = computed(() => {
  if (focused.value) {
    return {
      width: `${sceneWidth * scale.value}px`,
      height: `${sceneHeight * scale.value}px`,
      transform: `translateX(${focusedOffsetX.value}px)`
    }
  } else {
    return {
      width: `${sceneWidth * scale.value}px`,
      height: `${sceneHeight * scale.value}px`,
      transform: `translateX(${offsetX.value}px)`
    }
  }
})

const backgroundStyle = computed(() => ({
  width: `${sceneWidth * 0.6 * scale.value}px`,
}))

function npcStyle(npc: any) {
  const scaledX = npc.x * scale.value
  const scaledY = npc.y * scale.value
  const scaledScale = npc.scale * scale.value

  return {
    // position: 'absolute',
    left: `${scaledX}px`,
    top: `${scaledY}px`,
    transform: `translate(-50%, -50%) scale(${scaledScale})`,
    zIndex: npc.z
  }
}

const focusedNpcName = computed(() =>
  npcs.find(n => n.id === focusedNpc.value)?.name || ''
)
const focusedNpcImage = computed(() =>
  npcs.find(n => n.id === focusedNpc.value)?.img || ''
)

async function ask(input: string) {
  userInput.value = input
  loading.value = true
  response.value = ''

  const payload = {
    npcId: focusedNpc.value,
    // userId: 'guest',
    // sceneId: 'party_2nd_congress',
    question: userInput.value
  }

  userInput.value = ''

  if (!socket || socket.readyState !== WebSocket.OPEN) {
    socket = new WebSocket('ws://86.38.216.193:8000/ws/ask')  // 后端地址
    // socket = new WebSocket('ws://localhost:8000/ws/ask')  // 后端地址
    await new Promise((resolve, reject) => {
      socket!.onopen = resolve
      socket!.onerror = reject
    })
  }

  socket.send(JSON.stringify(payload))

  isTyping.value = true
  response.value = ''

  socket.onmessage = (event) => {
    const msg = event.data
    if (msg === '' || msg === "[[DONE]]") {
      // isTyping.value = false
      // loading.value = false
      return
    }
    loading.value = true
    // 流式追加内容，每次来一个片段就打字
    // await typewriterEffect(msg)
    enqueueMessage(msg)
  }

  socket.onerror = (err) => {
    console.error('WebSocket错误', err)
    isTyping.value = false
    loading.value = false
  }

  socket.onclose = () => {
    console.log('WebSocket连接关闭')
    isTyping.value = false
    loading.value = false
  }
}

const messageQueue = ref<string[]>([])
let rafId: number | null = null

function enqueueMessage(text: string) {
  messageQueue.value.push(...text.split(''))
  if (!rafId) {
    rafId = requestAnimationFrame(typewriterFrame)
  }
}

const SPEED = 3  // 每帧输出 3 个字（可以调成 2, 5, 10...）

function typewriterFrame() {
  for (let i = 0; i < SPEED; i++) {
    const nextChar = messageQueue.value.shift()
    if (nextChar) {
      response.value += nextChar
      if (dialogueContent.value) {
        dialogueContent.value.scrollTop = dialogueContent.value.scrollHeight
      }
    } else {
      rafId = null
      isTyping.value = false
      loading.value = false
      return  // 没有字了就退出，不要再循环
    }
  }

  rafId = requestAnimationFrame(typewriterFrame)
}

async function typewriterEffect(text: string) {
  for (let i = 0; i < text.length; i++) {
    if (!isTyping.value) {  // 如果被打断，直接退出
      response.value += text.slice(i)  // 补上剩余
      break
    }
    response.value += text[i]
    await new Promise(resolve => setTimeout(resolve, 20))  // 20ms一个字，更顺滑
    if (dialogueContent.value) {
      dialogueContent.value.scrollTop = dialogueContent.value.scrollHeight
    }
  }
}

function enterQuiz() {
  game.currentVideo = 'intro2'
  game.nextScene = 'quiz'
  game.goTo('intro')
}
</script>

<style scoped>
.scene {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.world-wrapper {
  width: 4000px;
  height: 100%;
  position: relative;
  transition: filter 0.3s ease;
}

.world-wrapper.blurred {
  filter: blur(5px);
}

.world-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 4000px;
  height: 100%;
  object-fit: cover;
  z-index: 0;
  pointer-events: none;
}

.npc {
  position: absolute;
  width: 400px;
  height: 1200px;
  z-index: 1;
}

.npc img {
  width: 100%;
  height: 100%;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.npc img.highlight {
  transform: scale(1.1);
  filter: drop-shadow(0 0 10px gold);
}

.awake-btn {
  float: left;
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 1;
  color: white;
  font-size: 40px;
  font-weight: bold;
  font-style: italic;
  background-color: transparent;
  border: none;
  cursor: pointer;
  animation: breathe 2s infinite alternate;
}

@keyframes breathe {
  0% {
    transform: scale(0.9);
  }

  100% {
    transform: scale(1.1);
  }
}
</style>