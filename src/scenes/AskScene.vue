<template>
  <div class="scene world-scene" @mousemove="handleMouseMove">
    <div class="world-wrapper" :class="{ blurred: focused }" :style="wrapperStyle" ref="wrapper">
      <img src="/assets/backgrounds/history-scene.jpg" class="world-background" :style="backgroundStyle" />
      <div v-for="npc in npcs" :key="npc.id" v-show="npc.visible" class="npc" :style="npcStyle(npc)"
        @mouseenter="hoveredNpc = npc.id" @mouseleave="hoveredNpc = null" @click="selectNpc(npc.id)">
        <img :src="npc.img" :class="{ highlight: hoveredNpc === npc.id }" />
      </div>
    </div>
    <!-- 修改为 fix 模式并添加 fixText -->
    <DialogueOverlay 
      :visible="focused" 
      :npcName="focusedNpcName" 
      :npcImage="focusedNpcImage" 
      :response="response"
      :loading="loading" 
      mode="fix" 
      :fixText="fixText" 
      @ask="ask" 
      @return="clearFocus" 
    />
    <button class="awake-btn" @click="enterNextScene">继续 ></button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted,provide } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import { useGameStore } from '../stores/game'
import { usePuzzleStore } from '../stores/puzzle'

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
 
// 生成密码的逻辑保持不变
const answer = generateAnswer();
const tips = generateTips(answer);
let puzzleAnswer = ""
for(let i = 0; i < 5; i++) {
  puzzleAnswer = puzzleAnswer + String.fromCharCode(answer[i]['数字'] + 48)
}

// 使用 store
const puzzleStore = usePuzzleStore()
// 将生成的密码存入 store
puzzleStore.setCorrectAnswer(puzzleAnswer)
// 修改NPC的fix文本为谜题提示
const npcFixTexts = {
  'chen_duxiu': generateTipForNpc(0),
  'zhang_guotao': generateTipForNpc(1),
  'li_da': generateTipForNpc(2),
  'yang_mingzhai': generateTipForNpc(3),
  'luo_zhanglong': generateTipForNpc(4),
  'wang_jinmei': generateTipForNpc(5),
  'xu_baihao': generateTipForNpc(6),
  'cai_hesen': generateTipForNpc(7),
  'tan_pingshan': generateTipForNpc(8),
  'li_zhenying': generateTipForNpc(9),
  'shi_cuntong': generateTipForNpc(10)
}

// 生成随机答案
function generateAnswer() {
  const color = ['红', '蓝', '绿', '黄', '紫'];
  const math = [1, 3, 5, 7, 9];
  const shape = ['圆形', '方形', '三角', '星形', '十字'];
  const material = ['金属', '木材', '玻璃', '塑料', '陶瓷'];
  const location = ['左一', '左二', '中间', '右二', '右一'];

  // 打乱属性数组
  [color, math, shape, material].forEach(arr => shuffleArray(arr));

  // 构建答案
  const answer = [];
  for (let i = 0; i < 5; i++) {
    answer.push({
      位置: location[i],
      颜色: color[i],
      数字: math[i],
      形状: shape[i],
      材料: material[i]
    });
  }
  return answer;
}

// 生成提示线索
function generateTips(answer: any[]) {
  const tips = [];

  tips.push(`数字${answer[0].数字}是${answer[0].颜色}色的，并且在${answer[0].位置}的位置`);
  tips.push(`数字${answer[2].数字}是${answer[2].材料}的`);
  tips.push(`数字${answer[4].数字}是${answer[4].形状}的，并且在${answer[4].位置}的位置`);
  tips.push(`${answer[3].颜色}的数字在${answer[4].颜色}的数字的右侧`);
  tips.push(`数字${answer[1].数字}是${answer[1].材料}的`);
  tips.push(`数字${answer[3].数字}是${answer[3].形状}的`);
  tips.push(`${answer[2].形状}的数字与${answer[0].材料}的数字相差${answer[2].数字-answer[0].数字}且${answer[0].材料}的数字在${answer[1].形状}的数字的左侧`);
  tips.push(`${answer[1].材料}的数字与${answer[2].形状}的数字相差${answer[1].数字-answer[2].数字}`);
  tips.push(`${answer[2].位置}的数字是${answer[2].形状}的`);
  tips.push(`${answer[3].位置}的数字是${answer[3].材料}的`);
  tips.push(`数字${answer[3].数字}在数字${answer[4].数字}的左侧且${answer[1].位置}的数字是${answer[1].颜色}色的`);

  return tips;
}

// 数组随机排序
function shuffleArray(array: any[]) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// 为NPC分配提示
function generateTipForNpc(index: number) {
  // 如果NPC数量多于提示数量，循环使用提示
  return tips[index % tips.length];
}
 
let socket: WebSocket | null = null
type NpcId = 
  | 'chen_duxiu' 
  | 'zhang_guotao' 
  | 'li_da' 
  | 'yang_mingzhai' 
  | 'luo_zhanglong' 
  | 'wang_jinmei' 
  | 'xu_baihao' 
  | 'cai_hesen' 
  | 'tan_pingshan' 
  | 'li_zhenying' 
  | 'shi_cuntong';
 
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
 
// 计算属性获取当前NPC的fix文本
const fixText = computed(() => {

  return focusedNpc.value ? npcFixTexts[focusedNpc.value as NpcId] : '这是修复模式的提示文本';

});
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
    question: userInput.value
  }
 
  userInput.value = ''
 
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    socket = new WebSocket('ws://localhost:8000/ws/ask')  // 后端地址
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
      isTyping.value = false
      return
    }
    loading.value = true
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
      if (!isTyping.value)
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
 
function enterNextScene() {
    game.currentVideo = 'intro2'
    game.nextScene = 'safe'
    game.goTo('safe')
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