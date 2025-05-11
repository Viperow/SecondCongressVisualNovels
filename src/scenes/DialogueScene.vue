<template>
  <div class="scene dialogue-scene">
    <h3>与 {{ npcId }} 对话中</h3>
    <textarea v-model="userInput" placeholder="请输入你的问题..."></textarea>
    <button @click="ask">提问</button>

    <div v-if="response" class="reply-box">
      <strong>NPC 回答：</strong>
      <p>{{ response }}</p>
    </div>

    <div v-if="loading">思考中...</div>

    <button @click="close">返回</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useGameStore } from '../stores/game'

const game = useGameStore()
const npcId = game.focusedNpc || 'unknown'
const userInput = ref('')
const response = ref('')
const loading = ref(false)

function getUserId() {
  let uid = localStorage.getItem('uid')
  if (!uid) {
    uid = 'user_' + Math.random().toString(36).slice(2, 10)
    localStorage.setItem('uid', uid)
  }
  return uid
}

async function ask() {
  loading.value = true
  response.value = ''

  const payload = {
    npcId,
    userId: getUserId(),
    sceneId: 'party_2nd_congress',
    question: userInput.value
  }

  try {
    const res = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    //{
    //   "reply": "我最深刻的印象是我们党第一次明确提出了民主集中制的组织原则。",
    //   "emotion": "serious",
    //   "voice": {
    //     "text": "我最深刻的印象是我们党第一次明确提出了民主集中制的组织原则。",
    //     "url": "https://your-api.com/audio/mao-12345.mp3"
    //   },
    //   "action": {
    //     "pose": "talking",
    //     "expression": "serious"
    //   },
    //   "meta": {
    //     "npcId": "mao_zedong",
    //     "model": "glm-4",
    //     "timestamp": "2025-04-12T15:00:00Z"
    //   }
    // }
    const result = await res.json()
    response.value = result.reply

    if (result.voice?.url) {
      const audio = new Audio(result.voice.url)
      audio.play()
    } else {
      speak(result.voice?.text || result.reply)
    }

  } catch (err) {
    console.error('AI 请求失败:', err)
    response.value = '（AI接口异常，请稍后重试）'
  } finally {
    loading.value = false
  }
}

function speak(text: string) {
  const utter = new SpeechSynthesisUtterance(text)
  utter.lang = 'zh-CN'
  speechSynthesis.cancel()
  speechSynthesis.speak(utter)
}

function close() {
  game.unfocusNpc()
}
</script>

<style scoped>
.scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

textarea {
  width: 80%;
  height: 100px;
  margin: 1rem 0;
}

button {
  margin: 0.5rem;
}

.reply-box {
  background: #f8f8f8;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  width: 80%;
}
</style>