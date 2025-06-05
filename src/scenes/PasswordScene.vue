<template>
    <div class="morse-scene">
        <img class="background" src="/assets/backgrounds/history-scene.jpg" />

        <DialogueOverlay :visible="showDialogue1" :npcName="npcName_1" :npcImage="npcImage_1" :loading="false"
            :steps="introSteps" :response="''" mode="choice" @end="onFirstDialogueEnd" />
        <DialogueOverlay :visible="showDialogue2" :npcName="npcName_2" :npcImage="npcImage_2" :loading="false"
            :steps="nextSteps" :response="''" mode="choice" @end="onDialogueEnd" />
        <button v-show="gameFinished" class="awake-btn" @click="enterNextScene">继续 ></button>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import type { DialogueStep } from '../stores/types'
import { useGameStore } from '../stores/game'

const game = useGameStore()
const showDialogue1 = ref(true)
const showDialogue2 = ref(false)
const npcName_1 = ref('陈独秀')
const npcImage_1 = ref('/assets/characters/chen_duxiu.png')
const npcName_2 = ref('蔡和森')
const npcImage_2 = ref('/assets/characters/cai_hesen.png')
const gameFinished = ref(false)

const introSteps: DialogueStep[] = [
{
type: 'text',
content: '同志，我是负责保管密码箱的负责人。最近组织安排我可能要外出执行任务，我担心我不在的时候同志们需要紧急取用文件',
image: ''
},
{
type: 'text',
content: '所以我特意设计了这个五位密码箱，每位密码都有颜色、数字、形状和材料四种属性。我把密码线索分散留给了几位可靠的同志',
image: ''
},
{
type: 'text',
content: '每位密码的属性组合如下：\n颜色（红、蓝、绿、黄、紫）\n数字（1、3、5、7、9）\n形状（圆形、方形、三角、星形、十字）\n材料（金属、木材、玻璃、塑料、陶瓷）',
image: ''
},
{
type: 'text',
content: '这个密码箱关系到组织的机密文件，一定要谨慎行事。',
image: ''
}
]

const nextSteps: DialogueStep[] = [
{
type: 'text',
content: '我们再次遇到搜捕了，需要将密码箱里的东西进行转移。因为需要人偷偷地进行转移，我们不能带着密码箱走，为了安全起见，密码的线索分给了我们所有人，还好我们现在都在，现在我们只需要将线索串起来就可以了',
image: ''
},
{
type: 'text',
content: '因为需要人偷偷地进行转移，我们不能带着密码箱走。',
image: ''
},
{
type: 'text',
content: '为了安全起见，密码的线索分给了我们所有人，还好我们现在都在，现在请你将线索串起来，找出密码。',
image: ''
}
]

function onFirstDialogueEnd() {
    showDialogue1.value = false  // 隐藏第一个对话
    showDialogue2.value = true   // 显示第二个对话
}

function onDialogueEnd() {
    gameFinished.value = true
}

function enterNextScene() {
    game.currentVideo = 'intro2'
    game.nextScene = 'ask'
    game.goTo('ask')
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