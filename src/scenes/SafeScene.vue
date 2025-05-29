<template>
    <div class="safe-scene">
        <img class="background" src="/assets/backgrounds/history-scene.jpg">
        
        <!-- 初始对话 -->
        <DialogueOverlay :visible="showDialogue" :npcName="npcName" :npcImage="npcImage" :loading="false"
            :steps="introSteps" :response="''" mode="choice" @end="startSafeGame" />
            
        <!-- 完成对话 -->
        <DialogueOverlay :visible="gameFinished" :npcName="npcName" :npcImage="npcImage" :loading="false"
            :steps="finishSteps" :response="''" mode="choice" @end="" />
            
        <!-- 游戏主界面 -->
        <div v-if="showSafeGame && !gameFinished" class="safe-game">
            <!-- 保险箱和密码显示 -->
            <div class="safe-container">
                <img 
                    class="safe-image" 
                    :src="safeOpened ? '/assets/Password/safebox_open.png' : '/assets/Password/safebox_close.png'" 
                    @click="focusOnSafe"
                    alt="密码箱"
                >
                <div class="code-display">{{ codeInput }}</div>
            </div>
            
            <!-- 数字键盘 -->
            <div class="safe-keypad" v-if="isSafeFocused">
                <div class="keypad-row" v-for="(row, i) in keypad" :key="i">
                    <button v-for="num in row" :key="num" @click="enterCode(num)" class="keypad-button">
                        {{ num }}
                    </button>
                </div>
                <button @click="clearCode" class="keypad-button clear-btn">清除</button>
                <button @click="submitCode" class="keypad-button submit-btn">确认</button>
            </div>
        </div>
        
        <button v-show="showBackButton" class="back-btn" @click="enterBeforeScene">← 回退</button>
        <button v-show="gameFinished" class="awake-btn" @click="enterNextScene">继续 ></button>
    </div>
</template>

<script setup lang="ts">
import { ref,inject } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import type { DialogueStep } from '../stores/types'
import { useGameStore } from '../stores/game'
import { usePuzzleStore } from '../stores/puzzle'

const game = useGameStore()
const showDialogue = ref(true)
const showSafeGame = ref(false)
const npcName = ref('张国焘')
const npcImage = ref('/assets/characters/zhang_guotao.png')
const gameFinished = ref(false)

// 游戏状态
const safeOpened = ref(false)
const isSafeFocused = ref(false)
const codeInput = ref('')
// 获取 store 实例
const puzzleStore = usePuzzleStore()

// 从 store 中获取正确密码
const correctCode = puzzleStore.correctAnswer

// 数字键盘布局
const keypad = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

const introSteps: DialogueStep[] = [
    {
        type: 'text',
        content: '同志，陈同志临走前交代，如果你能收集齐所有线索并推断出密码，就由你来负责保管这个密码箱。',
        image: ''
    },
    {
        type: 'text',
        content: '现在看起来你已经掌握了所有必要的线索，是时候尝试打开密码箱了。',
        image: ''
    },
]

const finishSteps: DialogueStep[] = [
    {
        type: 'text',
        content: '太好了！你成功打开了密码箱，取出了重要文件。',
        image: ''
    },
    {
        type: 'text',
        content: '陈同志知道一定会有人能解开这个密码，看来他没有看错人。从现在起，密码箱的保管工作就交给你了。',
        image: ''
    }
]

function startSafeGame() {
    showDialogue.value = false
    showSafeGame.value = true
}

function focusOnSafe() {
    isSafeFocused.value = true
}

function enterCode(num: string) {
    if (codeInput.value.length < 5) {
        codeInput.value += num
    }
}

function clearCode() {
    codeInput.value = ''
}
const showBackButton = ref(false) // 新增状态控制回退按钮显示

function submitCode() {
  if (puzzleStore.checkAnswer(codeInput.value)) {
    safeOpened.value = true
    gameFinished.value = true
    showBackButton.value = false
  } else {
    alert('密码错误！请再试一次')
    codeInput.value = ''
    showBackButton.value = true
  }
  isSafeFocused.value = false
}
function enterNextScene() {
    game.currentVideo = 'intro2'
    game.nextScene = 'quiz'
    game.goTo('intro')
}

function enterBeforeScene() {
    game.currentVideo = 'intro2'
    game.nextScene = 'ask'
    game.goTo('ask')
}
</script>
<style scoped>
.safe-scene {
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

.safe-game {
    position: fixed;  /* 改为固定定位 */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    display: flex;
    justify-content: center;
    align-items: center;
}

.safe-container {
    position: fixed;  /* 改为固定定位 */
    left: calc(40% - 200px);  /* 精确控制水平位置 */
    top: 60%;  /* 固定在垂直中间 */
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.safe-image {
    width: 300px;
    height: auto;
    cursor: pointer;
}

.code-display {
    position: fixed; /* 改为固定定位 */
    left: calc(45% - 75px); /* 居中定位，150px宽度的一半 */
    top: calc(50% + 100px); /* 保险箱下方100px处 */
    font-size: 24px;
    letter-spacing: 5px;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 5px;
    color: #0f0;
    font-family: monospace;
    min-width: 150px;
    text-align: center;
    z-index: 20; /* 确保在最上层 */
}

.safe-keypad {
    position: fixed;  /* 改为固定定位 */
    left: calc(40% + 150px);  /* 从中心向右偏移 */
    top: 60%;  /* 固定在垂直中间 */
    transform: translateY(-50%);
    background-color: rgba(0, 0, 0, 0.7);
    padding: 15px;
    border-radius: 10px;
    display: grid;
    grid-template-columns: repeat(3, 60px);
    gap: 10px;
}

.keypad-row {
    display: contents;
}

.keypad-button {
    width: 60px;
    height: 60px;
    font-size: 24px;
    border: none;
    border-radius: 5px;
    background-color: #444;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
}

.keypad-button:hover {
    background-color: #555;
}

.clear-btn, .submit-btn {
    grid-column: span 3;
    width: auto;
    background-color: #d9534f;
}

.submit-btn {
    background-color: #5cb85c;
}

.awake-btn {
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

.back-btn {
     position: absolute;
    top: 20px;
    left: 20px;
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