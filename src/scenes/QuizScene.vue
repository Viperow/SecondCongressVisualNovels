<template>
    <div class="quiz-scene">
        <img class="scene-background" src="/assets/backgrounds/quiz-scene.png" />

        <DialogueOverlay :visible="showDialogue" :npcName="currentNpcName" :npcImage="npcImage" :loading="loading"
            :steps="currentSteps" mode="choice" @end="handleDialogueEnd" @correct="countCorrect" />
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import type { DialogueStep } from '../stores/types'
import { useGameStore } from '../stores/game'

const game = useGameStore()
const showDialogue = ref(true)
const npcVisible = ref(true)
const currentNpcName = ref('老师')
const npcImage = ref('/assets/characters/teacher_ask.png')
const loading = ref(false)
const correctTime = ref(0)

// 题组
const currentSteps = ref<DialogueStep[]>([])
onMounted(async () => {
    const response = await fetch('/assets/text/questions.jsonl')
    const text = await response.text()
    currentSteps.value.push({
        type: 'choice',
        content: '后面的那位同学，请问你是睡着了吗？',
        options: ['老师，我听的太入迷了，遨游在知识的海洋里，沉浸在历史的长河中', '对啊，老师你讲的实在是太无聊了'],
        answer: 0,
        correctResponse: '好好好，那我有必要给你个舞台让你表演一下！',
        wrongResponse: '如此说来，想必你对这部分的知识了如指掌，我就出几道题考考你，答对了就放过你。',
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        image: '/assets/characters/teacher_ask.png',
    })
    currentSteps.value = currentSteps.value.concat(loadQuestionsFromJsonlText(text, 5))
    currentSteps.value.push({
        type: 'text',
        content: '我就先问这么多，不管刚才有没有睡觉，希望同学你能再接再厉，以后认真听课。'
    })
})

function loadQuestionsFromJsonlText(text: string, count: number): DialogueStep[] {
    const lines = text.trim().split('\n')
    const questions = lines.map(line => JSON.parse(line))
    const selected = shuffleArray(questions).slice(0, count)

    return selected.map((q) => ({
        type: 'choice',
        content: q.content,
        options: q.options,
        answer: q.answer,
        correctResponse: '回答正确！干得漂亮！',
        wrongResponse: `很遗憾，正确答案是：${q.options[q.answer]}`,
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        effect: 'confetti'
    }))
}

function shuffleArray<T>(array: T[]): T[] {
    const copy = [...array]
    for (let i = copy.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
            ;[copy[i], copy[j]] = [copy[j], copy[i]]
    }
    return copy
}

function handleDialogueEnd() {
    showDialogue.value = false
    if (correctTime.value >= 5) {
        game.currentVideo = 'stinger'
        game.nextVideo = 'credits'
    }
    else {
        game.currentVideo = 'credits'
        game.nextVideo = ''
    }
    game.nextScene = 'start'
    game.goTo('intro');
}

function countCorrect() {
    correctTime.value++
}

</script>

<style scoped>
.quiz-scene {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    background-color: black;
}

.scene-background {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    z-index: 0;
}
</style>