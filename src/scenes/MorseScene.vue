<template>
    <div class="morse-scene">
        <img class="background" src="/assets/backgrounds/history-scene.jpg" />

        <DialogueOverlay :visible="showDialogue" :npcName="npcName" :npcImage="npcImage" :loading="false"
            :steps="introSteps" :response="''" mode="choice" @end="startMorseGame" />
        <DialogueOverlay :visible="gameFinished" :npcName="npcName" :npcImage="npcImage" :loading="false"
            :steps="finishSteps" :response="''" mode="choice" @end="" />
        <div v-if="showMorseGame && !gameFinished" class="morse-game">
            <div class="morse-target">请发送电报内容：<strong>{{ currentTarget.text }}</strong></div>
            <div class="morse-target"> S对应的摩斯密码是：... O对应的摩斯密码是：---<br>每个字母之间都要有简短的间隔<br>短按鼠标是.，长按是-</div>
            <div class="morse-input-display">{{ morseInput?.trim() }}</div>
            <button class="morse-press" @mousedown="startPress" @mouseup="endPress">按住发送</button>
            <div class="morse-actions">
                <button @click="submitMorse">提交</button>
                <button @click="resetMorse">重置</button>
            </div>
        </div>
        <button v-show="gameFinished" class="awake-btn" @click="enterNextScene">醒来 ></button>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import type { DialogueStep } from '../stores/types'
import { useGameStore } from '../stores/game'

const game = useGameStore()
const showDialogue = ref(true)
const showMorseGame = ref(false)
const isPressing = ref(false)
const npcName = ref('李达')
const npcImage = ref('/assets/characters/li_da.png')
const gameFinished = ref(false)

// onMounted(() => {
//     window.addEventListener('keydown', handleKeyDown)
//     window.addEventListener('keyup', handleKeyUp)
// })

// onUnmounted(() => {
//     window.removeEventListener('keydown', handleKeyDown)
//     window.removeEventListener('keyup', handleKeyUp)
// })

// function handleKeyDown(e: KeyboardEvent) {
//     if (e.code === 'Space' && !isPressing.value) {
//         e.preventDefault()
//         startPress()
//     }
// }

// function handleKeyUp(e: KeyboardEvent) {
//     if (e.code === 'Space' && isPressing.value) {
//         e.preventDefault()
//         endPress()
//     }
// }

const introSteps: DialogueStep[] = [
    {
        type: 'text',
        content: '同志，不好了，我们遭遇到了追捕，现在需要用电报机把求救信息发送给接应我们的同志。',
        image: '/assets/characters/li_da.png'
    },
    {
        type: 'text',
        content: '求救内容我一会告诉你，准备好了吗？',
        image: '/assets/characters/li_da.png'
    }
]

const finishSteps: DialogueStep[] = [
    {
        type: 'text',
        content: '太好了，求救信息发送成功了，我们的同志帮助我们躲避了追捕',
        image: '/assets/characters/li_da.png'
    },
]

function startMorseGame() {
    showDialogue.value = false
    showMorseGame.value = true
}

const currentTarget = ref({ text: 'SOS', code: '... --- ...' })
const morseInput = ref('')
let pressStartTime = 0
let lastReleaseTime = 0

function startPress() {
    pressStartTime = Date.now()
    isPressing.value = true
    playBeep()
}

function endPress() {
    stopBeep()
    const now = Date.now()
    const duration = now - pressStartTime

    const gap = lastReleaseTime > 0 ? now - lastReleaseTime - duration : 0
    if (gap > 1200) {
        morseInput.value += "   "
    } else if (gap > 600) {
        morseInput.value += ' '
    }

    morseInput.value += duration < 300 ? '.' : '-'
    lastReleaseTime = now
}

function submitMorse() {
    const cleanedInput = morseInput.value.trim()
    const cleanedTarget = currentTarget.value.code.trim()

    if (cleanedInput === cleanedTarget) {
        gameFinished.value = true
    } else {
        alert(`❌ 错误！应为 ${currentTarget.value.code}`)
    }
}

function resetMorse() {
    morseInput.value = ''
}

let beepOsc: OscillatorNode | null = null
function playBeep() {
    const audioCtx = new (window.AudioContext || window.AudioContext)()
    beepOsc = audioCtx.createOscillator()
    beepOsc.frequency.setValueAtTime(600, audioCtx.currentTime) // 600Hz Morse tone
    const gainNode = audioCtx.createGain()
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime)
    beepOsc.connect(gainNode).connect(audioCtx.destination)
    beepOsc.start()
}

function stopBeep() {
    if (beepOsc) {
        beepOsc.stop()
        beepOsc.disconnect()
        beepOsc = null
    }
}

function enterNextScene() {
    game.currentVideo = 'intro2'
    game.nextScene = 'quiz'
    game.goTo('intro')
}
</script>

<style scoped>
.morse-scene {
    position: relative;
    width: 100vw;
    height: 100vh;
    background-color: black;
    overflow: hidden;
    color: white;
}

.background {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 0;
}

.morse-game {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 1.5rem;
}

.morse-target {
    font-size: 1.8rem;
    margin-top: 1rem;
}

.morse-input-display {
    font-size: 2.5rem;
    letter-spacing: 1rem;
    margin: 1rem;
    padding: 0.5rem 1rem;
    border: 2px dashed white;
    border-radius: 8px;
    white-space: pre;
    /* 防止空格折叠 */
}

.morse-press {
    padding: 1rem 2rem;
    font-size: 1.5rem;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
    border: 2px solid white;
    cursor: pointer;
    transition: all 0.2s ease;
}

.morse-press:active {
    background-color: rgba(255, 255, 255, 0.4);
    transform: scale(0.95);
}

.morse-actions button {
    padding: 0.5rem 1.5rem;
    margin: 0 0.5rem;
    font-size: 1.2rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.15);
    color: white;
    transition: background 0.2s ease;
}

.morse-actions button:hover {
    background: rgba(255, 255, 255, 0.3);
}

.awake-btn {
    float: left;
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 99;
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
