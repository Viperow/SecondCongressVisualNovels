<template>
    <div class="quiz-scene">
        <img class="scene-background" src="/assets/backgrounds/quiz-scene.png" />

        <DialogueOverlay :visible="showDialogue" :npcName="currentNpcName" :npcImage="npcImage"
             :loading="loading" :steps="currentSteps" mode="choice"
            @end="handleDialogueEnd" @correct="countCorrect"/>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
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

// 示例题组
const currentSteps = ref<DialogueStep[]>([
    {
        type: 'choice',
        content: '后面的那位同学，请问你是睡着了吗？',
        options: ['老师，我听的太入迷了，遨游在知识的海洋里，沉浸在历史的长河中', '对啊，老师你讲的实在是太无聊了'],
        answer: 0,
        correctResponse: '好好好，那我有必要给你个舞台让你表演一下！',
        wrongResponse: '如此说来，想必你对这部分的知识了如指掌，我就出几道题考考你，答对了就放过你。',
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        image: '/assets/characters/teacher_ask.png',
    },
    {
        type: 'choice',
        content: '下列哪位是中国共产党的创始人之一？',
        options: ['鲁迅', '陈独秀', '李白'],
        answer: 1,
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        effect: 'confetti'
    },
    {
        type: 'choice',
        content: '下列哪位是中国共产党的创始人之一？',
        options: ['鲁迅', '陈独秀', '李白'],
        answer: 1,
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        effect: 'confetti'
    },    {
        type: 'choice',
        content: '下列哪位是中国共产党的创始人之一？',
        options: ['鲁迅', '陈独秀', '李白'],
        answer: 1,
        correctResponse: '答对了，继续加油！',
        wrongResponse: '很遗憾，正确答案是陈独秀。',
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        effect: 'confetti'
    },    {
        type: 'choice',
        content: '下列哪位是中国共产党的创始人之一？',
        options: ['鲁迅', '陈独秀', '李白'],
        answer: 1,
        correctResponse: '答对了，继续加油！',
        wrongResponse: '很遗憾，正确答案是陈独秀。',
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        effect: 'confetti'
    },    {
        type: 'choice',
        content: '下列哪位是中国共产党的创始人之一？',
        options: ['鲁迅', '陈独秀', '李白'],
        answer: 1,
        correctImage: '/assets/characters/teacher_cong.png',
        wrongImage: '/assets/characters/teacher_disap.png',
        correctSound: '/assets/sounds/correct.mp3',
        wrongSound: '/assets/sounds/wrong.mp3',
        effect: 'confetti'
    },
    {
        type: 'text',
        content: '我就先问这么多，不管刚才有没有睡觉，希望同学你能再接再厉，以后认真听课。'
    }
])

function handleDialogueEnd() {
    showDialogue.value = false
    if (correctTime.value >= 5){
        game.currentVideo  = 'stinger'
        game.nextVideo = 'credits'
    }
    else{
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