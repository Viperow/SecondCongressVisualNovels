<template>
    <div id="dialogue-scene" class="focus-overlay" v-if="visible" @click="onClick">
        <img v-if="npcImage && mode === 'choice' " :src="currentImage" class="focused-npc-image" />
        <img v-if="npcImage && mode === 'dialogue' " :src="npcImage" class="focused-npc-image" />

        <div class="dialogue-box">
            <div class="dialogue-header">{{ npcName }}</div>

            <div class="dialogue-content" ref="dialogueRef">
                <p>{{ currentText }}</p>
            </div>

            <div class="dialogue-input" v-if="mode === 'dialogue'">
                <textarea v-model="userInput" placeholder="请输入你的问题..." />
                <div class="dialogue-buttons">
                    <button @click="onAsk" :disabled="loading">{{ loading ? '思考中...' : '提问' }}</button>
                    <button @click="onReturn">返回</button>
                </div>
            </div>

        </div>

        <div v-if="mode === 'choice' && !showContinueHint" class="choice-overlay">
            <div class="choice-list">
                <button v-for="(opt, index) in currentStep?.options" :key="index" :class="{
                    selected: index === selectedIndex,
                    correct: selectedIndex !== null && index === currentStep?.answer,
                    wrong: selectedIndex === index && index !== currentStep?.answer
                }" @click.stop="selectChoice(index)">
                    {{ opt }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
import type { DialogueStep } from '../stores/types'

const props = defineProps<{
    visible: boolean
    npcName: string
    npcImage: string
    response?: string
    loading: boolean
    mode: 'dialogue' | 'choice'
    steps?: DialogueStep[]
}>()

const emits = defineEmits(['ask', 'return', 'choice', 'end', 'correct'])

const dialogueRef = ref<HTMLDivElement | null>(null)
const currentIndex = ref(0)
const selectedIndex = ref<number | null>(null)
const showContinueHint = ref(false)
const userInput = ref('')
// const defualtImage = computed(() => props.npcImage)
const currentImage = ref(props.npcImage)

const currentStep = computed(() => props.steps?.[currentIndex.value])
const currentText = computed(() => {
    if (!props.steps || props.steps.length === 0) return props.response
    return currentStep.value?.content || ''
})


// 点击“提问”时触发事件，向父组件发送内容
function onAsk() {
    if (!userInput.value.trim()) return
    emits('ask', userInput.value)
    userInput.value = ''  // 清空输入框
}

function onReturn() {
    emits('return')
}

function onClick() {
    // 留空或添加 isTyping 控制逻辑
    if (currentStep.value?.type === 'choice' && !showContinueHint.value) return

    if (props.steps && currentIndex.value < props.steps.length - 1) {
        currentIndex.value++
    } else {
        emits('end') // ✅ 这就是 emit('end')，确认它在最后一步时触发
    }
}

function selectChoice(index: number) {
    emits('choice', index)
    if (selectedIndex.value !== null || currentStep.value?.type !== 'choice') return
    selectedIndex.value = index

    const correct = index === currentStep.value?.answer

    if (correct) {
        if (currentStep.value?.correctSound) playSound(currentStep.value.correctSound)
        if (currentStep.value?.correctImage) currentImage.value = currentStep.value.correctImage
        if (currentStep.value?.effect === 'confetti') showParticles()
        props.steps![currentIndex.value].content = currentStep.value?.correctResponse || '恭喜你答对了！'
        emits('correct')
    } else {
        const answer = currentStep.value?.options?.[currentStep.value?.answer ?? 0]
        if (currentStep.value?.wrongSound) playSound(currentStep.value.wrongSound)
        if (currentStep.value?.wrongImage) currentImage.value = currentStep.value.wrongImage
        props.steps![currentIndex.value].content = currentStep.value?.wrongResponse || `很遗憾，回答错误，正确答案是：${answer}`
    }

    showContinueHint.value = true
}

function playSound(src?: string) {
    if (!src) return
    const audio = new Audio(src)
    audio.play()
}

function showParticles() {
    const el = document.createElement('div')
    el.className = 'confetti-effect'
    document.getElementById("dialogue-scene")?.appendChild(el)
    setTimeout(() => document.getElementById("dialogue-scene")?.removeChild(el), 2000)
}

watch(currentStep, async (step) => {
    selectedIndex.value = null
    showContinueHint.value = false
    currentImage.value = props.npcImage

    if (step?.sound) playSound(step.sound)
    if (step?.image) currentImage.value = step.image
    // if (step?.effect === 'confetti') showParticles()
    await nextTick()
    if (dialogueRef.value) {
        dialogueRef.value.scrollTop = dialogueRef.value.scrollHeight
    }
})
</script>

<style scoped>
/* 保留原 focus-overlay 样式 */
.focus-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(6px);
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.focus-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(6px);
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.focused-npc-image {
    width: auto;
    height: 180%;
    object-fit: contain;
    margin-top: 50rem;
}

.dialogue-box {
    position: absolute;
    bottom: 0;
    width: 90%;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    max-height: 40%;
    margin-bottom: 1rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.dialogue-header {
    margin-bottom: 2rem;
    text-align: left;
    /* 右对齐 */
    font-size: 1.8rem;
    font-weight: bolder;
    color: #fff;
    padding-left: 1rem;
}

.dialogue-content {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 0.5rem;
    width: 80%;
    margin: 0 auto 0.5rem;
    color: #ffffff;
    max-height: 150px;
    font-size: x-large;
}


.dialogue-content::-webkit-scrollbar {
    width: 6px;
}

.dialogue-content::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.2);
    border-radius: 3px;
}

.dialogue-input {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    /* 输入框和按钮之间留点缝隙 */
}

textarea {
    flex: 1;
    height: 120px;
    /* 只一行高度 */
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 0.5rem;
    font-size: 1.5rem;
    resize: none;
    color: white;
    background: rgba(255, 255, 255, 0.2);
}

textarea::placeholder {
    color: rgb(227, 227, 227);
}

.dialogue-buttons {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

button {
    height: 60px;
    padding: 0 1rem;
    border: none;
    border-radius: 8px;
    background-color: rgba(169, 151, 222, 0.196);
    color: white;
    font-size: 1.6rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

button:hover {
    background-color: #fbd0d07d;
}

button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
}

.choice-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20;
    pointer-events: none;
}

.choice-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 60%;
    align-items: center;
    pointer-events: auto;
}

.choice-list button {
    width: 100%;
    padding: 1rem 2rem;
    font-size: 1.6rem;
    background-color: rgba(255, 255, 255, 0.2);
    border: 2px solid white;
    border-radius: 12px;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.choice-list button:hover {
    background-color: rgba(255, 255, 255, 0.4);
    transform: scale(1.05);
}

.choice-list button.correct {
    background-color: rgba(0, 255, 0, 0.3);
}

.choice-list button.wrong {
    background-color: rgba(255, 0, 0, 0.3);
}

.choice-list button.selected {
    border: 2px solid #fff;
}

.confetti {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 300px;
    height: 300px;
    background-image: url('/assets/effects/confetti.gif');
    background-size: contain;
    background-repeat: no-repeat;
    transform: translate(-50%, -50%);
    pointer-events: none;
}
</style>