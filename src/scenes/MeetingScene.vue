<template>
  <div class="meeting-scene">
    <img class="background" src="/assets/backgrounds/history-scene.jpg" />
    <DialogueOverlay
      :key="`${part}-${isUserTurn}-${currentIndex}`"
      :visible="showDialogue"
      :npcName="npcName"
      :npcImage="npcImage"
      :response="response"
      :loading="loading"
      :mode="mode"
      :steps="mode === 'choice' ? steps : undefined"
      :returnButtonText= "'结束'"
      @ask="ask"
      @return="handleReturn"
      @end="handleEnd"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useGameStore } from '../stores/game'
import DialogueOverlay from '../components/DialogueOverlay.vue'
import type { DialogueStep } from '../stores/types'

const game = useGameStore()

const script1Before: DialogueStep[] = [
  { name: "陈独秀", type: "text", content: "同志们，根据党章规定，我们需要选举产生中央执行委员会，作为党的最高领导机关。全国党员人数已达195人，党组织已初步健全，是时候建立更完善的领导机制了。" },
  
]

const script1After: DialogueStep[] = [
  { name: "张国焘", type: "text", content: "我提议由陈先生担任中央执行委员会委员长。陈先生在党的一大就担任中央局书记，经验丰富，且有很高的威望。只有他能带领我们克服当前的困难。" },
  { name: "李达", type: "text", content: "张同志，我有个疑问。党章规定中央执行委员会由五人组成，另选候补委员三人。是否应该让更多地方代表参与决策？比如罗同志，他正在领导工人运动，实践经验很丰富。" },
  { name: "罗章龙", type: "text", content: "李同志说得有道理。不过我倒认为，当前形势复杂，确实需要有权威的中央领导。陈先生作为党的创始人之一，由他领导是合适的。" },
  { name: "王尽美", type: "text", content: "我支持陈先生。在上海工厂，工人们都在传颂陈先生的革命思想。有他在，我们的工人运动就有方向了。" },
  { name: "许白昊", type: "text", content: "是啊！陈先生的领导对湖北汉阳钢铁厂的罢工也起到了关键作用。没有中央的指导，我们工人是无法团结起来的。" },
  { name: "施存统", type: "text", content: "我提议立即进行选举，采用无记名投票的方式，确保公平公正。" },
  { name: "蔡和森", type: "text", content: "施同志的提议很好。我们既要民主选举，又要确保党的集中统一。无产阶级的革命事业容不得任何涣散和分裂。" },
  { name: "李震瀛", type: "text", content: "我同意。工人运动需要强有力的中央领导，才能协调各地的斗争。比如最近的京汉铁路罢工，就因缺乏统一指挥而受挫。" },
  { name: "杨明斋", type: "text", content: "我完全支持陈先生担任委员长。他在上海工人中有着极高的威望，能够有效指导各地工运。" },
  { name: "谭平山", type: "text", content: "陈先生的领导对推动国共合作至关重要。广东的工人运动已经与国民党建立了联系，需要中央统一指导。" },
  { name: "陈独秀", type: "text", content: "诸位的厚爱令我感激，但我必须说，我能力有限。不过既然组织信任我，我愿为党的事业鞠躬尽瘁。" },
  { name: "张国焘", type: "text", content: "现在开始投票选举中央执行委员会委员。请每位同志写下五位正式委员和三位候补委员的名字，放入票箱。" },
  { name: "全体代表", type: "text", content: "(票纸放入木制票箱的声响)" },
  { name: "陈独秀", type: "text", content: "我来唱票。陈独秀、张国焘、蔡和森、高君宇、邓中夏——五位正式委员。李大钊、向警予、张太雷——三位候补委员。全体一致通过！" },
  { name: "蔡和森", type: "text", content: "陈先生，请允许我负责党的宣传工作。我将组织起草《向导》周报，向全国工人农民宣传党的纲领。" },
  { name: "张国焘", type: "text", content: "我负责组织工作，确保各地党组织严格执行中央决议。各地的罢工斗争需要强有力的组织保障。" },
  { name: "陈独秀", type: "text", content: "很好。现在我们有了明确的领导机构，相信党的革命事业将迎来新的发展阶段。" },
  { name: "罗章龙", type: "text", content: "陈先生，我有个请求。中央执行委员会需要经常深入一线，了解工人的实际需求。比如最近的京汉铁路罢工，我们需要总结经验教训。" },
  { name: "陈独秀", type: "text", content: "罗同志说得对。我们将定期召开会议，听取各地斗争情况汇报。同时，中央执行委员会委员也要轮流下去指导工作。" },
  { name: "李达", type: "text", content: "我担心的是，中央执行委员会的权威如何与地方党组织的自主性协调？党章规定“全国代表大会为本党最高机关”，但平时中央执行委员会就是最高领导。" },
  { name: "蔡和森", type: "text", content: "李同志的问题很重要。我们的民主集中制原则就是答案——在民主基础上集中，在集中指导下民主。中央执行委员会的决议，地方党组织必须执行，但也要听取地方党组织的合理建议。" },
  { name: "陈独秀", type: "text", content: "让我们记住，我们不是为了权力而选举，而是为了革命事业的胜利。中央执行委员会将不负重托，领导全党团结一致，共同奋斗！" }
]

const script2Before: DialogueStep[] = [
  { name: '陈独秀', type: 'text', content: '(翻开宣言草案，语气庄重)：同志们，这是我们起草的《中国共产党宣言》初稿。宣言要解决两个问题：一是党的最高纲领，二是当前阶段的最低纲领。最高纲领是实现共产主义社会，这一点没有争议。但最低纲领的具体内容，我们需要深入讨论。' },
  { name: '蔡和森', type: 'text', content: '(条理清晰地)：根据列宁关于民族殖民地问题的理论，当前中国的首要任务是进行反帝反封建的民族民主革命，这与党的一大直接进行社会主义革命的主张有所不同。我建议在宣言中明确三个最低纲领：消除内乱，打倒军阀，建设国内和平；推翻国际帝国主义的压迫，达到中华民族完全独立；统一中国为真正的民主共和国。' },
  { name: '张国焘', type: 'text', content: '(语气务实)：蔡同志的建议很合理。但宣言还需要更具体的工人运动策略。比如，如何组织罢工，如何建立工会，这些都需要明确指导。' },
  { name: '王尽美', type: 'text', content: '(直率地)：是啊！在上海工厂，工人们最关心的是如何团结起来，对抗资本家和军阀。宣言要能激发工人的斗争热情，明确我们的目标。' },
  { name: '许白昊', type: 'text', content: '(激烈地)：我同意王同志的观点，但农民也不能被忽视！湖北的农民正在受地主剥削，宣言必须明确农民的土地诉求，否则我们将失去最庞大的革命力量。' },
  { name: '李达', type: 'text', content: '(理性地)：许同志的问题很有道理，但当前阶段，我们是否应该将农民土地问题直接写入宣言？土地改革可能需要更长时间的准备，当前我们应先解决军阀和帝国主义的问题。' },
  { name: '蔡和森', type: 'text', content: '(耐心解释)：李同志，你的担忧是合理的。土地问题是农民的核心关切，但现阶段我们与资产阶级民主派联合的策略，决定了宣言不能直接提出土地革命。我们可以在宣言中提出"废除丁漕等重税，规定全国城市及乡村的土地税则，推出限制田租率的法律"，为未来的土地改革做铺垫。' },
  { name: '张国焘', type: 'text', content: '(补充道)：我建议在宣言中明确工人运动的具体方向。比如，号召全国工人联合起来，建立统一的工人组织；组织罢工，反对资本家剥削；同时，也要强调工人阶级与农民阶级的联合。' },
  { name: '王尽美', type: 'text', content: '(兴奋地)：这个方向很好！在上海、济南的工厂，工人们已经开始组织起来。宣言要能为这些斗争提供理论指导和方向指引。' },
  { name: '许白昊', type: 'text', content: '(仍有些不满)：但农民怎么办？湖北汉阳钢铁厂的罢工失败，很大程度上是因为农民没有支持。只有解决土地问题，才能真正动员农民。' },
  { name: '蔡和森', type: 'text', content: '(坚定地)：许同志，我理解你的焦虑，但我们不能操之过急。根据列宁的理论，在半殖民地半封建的中国，无产阶级必须先联合资产阶级民主派进行反帝反封建的民主革命，待条件成熟再进行社会主义革命。土地问题可以在民主革命胜利后逐步解决。' },
  { name: '李达', type: 'text', content: '(若有所思)：我还有一个疑问。宣言中提出的"民主共和国"，是否意味着让资产阶级掌握政权？这会不会导致工人阶级被出卖？ 在法国大革命中，资产阶级就曾背叛无产阶级。' },
  { name: '蔡和森', type: 'text', content: '(耐心解释)：李同志，你的问题触及了革命的精髓。民主共和国不是让资产阶级掌握政权，而是建立一个工人、农民和小资产阶级联合的政权。正如列宁所说，在民族民主革命中，无产阶级必须保持自己的独立性，不能被资产阶级所利用。' },
  { name: '张国焘', type: 'text', content: '(强调道)：我完全同意蔡同志的观点。工人阶级必须是革命的领导力量，联合农民和小资产阶级，共同推翻帝国主义和封建军阀的统治。在宣言中，我们需要明确这一点。' },
  { name: '谭平山', type: 'text', content: '(策略性地)：蔡同志，张同志，我有一个补充建议。国民党作为资产阶级民主派的代表，是我们重要的联合对象。宣言中应该提到邀请国民党等革命团体举行联席会议，共商合作事宜。' },
  { name: '李达', type: 'text', content: '(谨慎地)：谭同志，我担心国民党并不像我们想象的那样革命。如果联合国民党，是否会导致我们的革命方向被扭曲？ 一大的时候，我们曾规定"不同其他党派建立任何关系"。' },
  { name: '蔡和森', type: 'text', content: '(理性地)：李同志，你记得的没错。但形势已经发生了变化。一方面，共产国际明确指示我们与国民党合作；另一方面，工人运动屡遭镇压，我们需要更广泛的力量支持。正如陈先生在《中国共产党对于时局的主张》中所说，"无产阶级未能获得政权以前，依中国政治经济的现状，依历史进化的过程，无产阶级在目前最切要的工作，还应该联络民主派共同对封建式的军阀革命"。' },
  { name: '陈独秀', type: 'text', content: '(总结道)：蔡同志的分析很透彻。我们的联合战线是有原则的联合，是独立自主的联合。国民党必须接受我们的革命纲领，而不是我们去迁就他们。' },
  { name: '施存统', type: 'text', content: '(热情洋溢地)：我建议宣言要更充满战斗性！要像一把火，点燃全国青年的革命热情。比如，可以加入"青年要觉醒，青年要奋斗，青年要为民族独立和人民解放而战"这样的口号。' },
  { name: '杨明斋', type: 'text', content: '(温和地)：施同志的提议很好，但宣言的语言也要通俗易懂，让工人农民都能理解。比如"真正的民主共和国"是什么意思？需要更具体的解释。' },
  { name: '蔡和森', type: 'text', content: '(思考片刻)：杨同志说得对。革命宣言不仅要坚定有力，还要贴近群众。我们可以这样表述："真正的民主共和国，就是推翻帝国主义和封建军阀的统治，建立一个由工人、农民和小资产阶级共同参与的政权"。' },
  { name: '张国焘', type: 'text', content: '(务实地)：我建议在宣言中加入具体的工作方法，比如"组织工会，建立工人学校，培养工人骨干"。没有具体的实践指导，宣言只是一纸空文。' },
  { name: '王尽美', type: 'text', content: '(支持地)：是的！在上海、济南的工厂，工人们需要明确的行动指引。宣言要能回答工人们的问题：我们该怎么做？。' },
  { name: '罗章龙', type: 'text', content: '(补充道)：我同意张同志的观点。工人运动需要强有力的组织保障。比如，可以提出"建立全国统一的工人组织，定期召开工人代表大会"。' },
  { name: '李震瀛', type: 'text', content: '(务实地)：我建议宣言中加入"联合一切被压迫阶级和阶层，包括手工业者、小店主、小雇主等小资产阶级"。只有广泛团结一切进步力量，才能形成强大的革命合力。' },
  { name: '陈独秀', type: 'text', content: '(满意地)：各位的讨论很有价值。宣言既要坚持马克思主义的革命原则，又要结合中国的实际国情。现在，请蔡同志和张同志继续完善宣言草案，明天提交大会表决。' },
  { name: '蔡和森', type: 'text', content: '(自信地)：我们一定不负众望。宣言将是中国共产党对中华民族前途命运的深刻思考，也将是指导全国革命斗争的纲领性文件。' },
  { name: '张国焘', type: 'text', content: '(坚定地)：我们还需要考虑宣言的宣传方式。不能只是知识分子看懂，工人农民也要能听懂。可以简化一些术语，用更通俗的语言表达。' },
  { name: '王尽美', type: 'text', content: '(支持地)：是的！在上海工厂，我们经常用通俗的话向工人讲解革命道理。宣言要能唤醒工人的阶级意识，激发他们的斗争热情。' },
  { name: '许白昊', type: 'text', content: '(仍有些担忧)：但农民怎么办？宣言中必须提到农民的土地问题，否则农民不会支持我们。' },
  { name: '蔡和森', type: 'text', content: '(安抚地)：许同志，请放心。我们会在《关于"民主的联合战线"的议决案》中详细阐述农民问题。在宣言中，我们可以用"三万万的农民，他们是革命运动中的最大要素"这样的表述，强调农民的重要性。' },
  { name: '陈独秀', type: 'text', content: '(总结道)：让我们记住，宣言不仅是对革命目标的阐述，更是对革命道路的指引。中国共产党将领导工人、农民和小资产阶级，共同推翻帝国主义和封建军阀的统治，建立真正的民主共和国。这是我们的历史使命，也是我们的坚定信念！' }
]

const script2After: DialogueStep[] = [
  { name: '陈独秀', type: 'text', content: '很好，希望你继续努力，为革命事业贡献力量。' }
]

const scripts: Record<number, [DialogueStep[], DialogueStep[]]> = {
  1: [script1Before, script1After],
  2: [script2Before, script2After]
}

const part = ref<0 | 1>(0)
const currentIndex = ref(0)
const scriptPair = computed(() => scripts[game.meetingTime] || scripts[1])
const currentScript = computed(() => scriptPair.value[part.value])
const currentLine = computed(() => currentScript.value[currentIndex.value])
const lastSpeaker = ref('')
const isUserTurn = ref(false)

const showDialogue = ref(true)
const response = ref('')
const loading = ref(false)
const isTyping = ref(false)
let socket: WebSocket | null = null

const npcImages: Record<string, string> = {
  '陈独秀': '/assets/characters/chen_duxiu.png',
  '张国焘': '/assets/characters/zhang_guotao.png',
  '李达': '/assets/characters/li_da.png',
  '杨明斋': '/assets/characters/yang_mingzhai.png',
  '罗章龙': '/assets/characters/luo_zhanglong.png',
  '王尽美': '/assets/characters/wang_jinmei.png',
  '许白昊': '/assets/characters/xu_baihao.png',
  '蔡和森': '/assets/characters/cai_hesen.png',
  '谭平山': '/assets/characters/tan_pingshan.png',
  '李震瀛': '/assets/characters/li_zhenying.png',
  '施存统': '/assets/characters/shi_cuntong.png'
}

// const npcName = computed(() => {
//   if (isUserTurn.value) return lastSpeaker.value
//   return currentLine.value?.name || ''
// })
const npcRandomizer = ref(0)
const npcName = computed(() => {
  npcRandomizer.value
  if (isUserTurn.value) {
    const npcKeys = Object.keys(npcImages)
    const randomIndex = Math.floor(Math.random() * npcKeys.length)
    return npcKeys[randomIndex]
  }
  console.log('当前回答者:', currentLine.value.name)
  if (game.meetingTime === 1 && currentLine.value?.name === "陈独秀") currentLine.value.name = "李达"
  return currentLine.value?.name || ''
})
const npcImage = computed(() => npcImages[npcName.value] || '')
const mode = computed(() => (isUserTurn.value ? 'dialogue' : 'choice'))
const steps = computed<DialogueStep[]>(() => [
  {
    name: currentLine.value?.name,
    type: 'text',
    content: currentLine.value?.content || '',
  },
])
async function ask(question: string) {
  loading.value = true
  response.value = ''

  npcRandomizer.value++ 

  if (!socket || socket.readyState !== WebSocket.OPEN) {
    socket = new WebSocket('ws://localhost:10081/ws/manus')
    await new Promise((resolve, reject) => {
      socket!.onopen = resolve
      socket!.onerror = reject
    })
    socket.onmessage = handleMessage
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

  socket.send(JSON.stringify({ question }))
  isTyping.value = true
}

const messageQueue = ref<string[]>([])
let rafId: number | null = null

function handleMessage(event: MessageEvent) {
  const msg = event.data
  console.log('当前回答:', msg)
  if (msg === '' || msg === '[[DONE]]') {
    isTyping.value = false
    return
  }
  if (msg === '互动已经完成，状态为：success') {
    handleReturn();
    isTyping.value = false
    return
  }
  enqueueMessage(msg)
}

function enqueueMessage(text: string) {
  messageQueue.value.push(...text.split(''))
  if (!rafId) {
    rafId = requestAnimationFrame(typewriterFrame)
  }
}

const SPEED = 3
function typewriterFrame() {
  for (let i = 0; i < SPEED; i++) {
    const ch = messageQueue.value.shift()
    if (ch) {
      response.value += ch
    } else {
      rafId = null
      if (!isTyping.value) loading.value = false
      return
    }
  }
  rafId = requestAnimationFrame(typewriterFrame)
}

function handleEnd() {
  nextLine()
}

function handleReturn() {
  if (mode.value === 'dialogue') {
    isUserTurn.value = false
    part.value = 1
    currentIndex.value = 0
  }
}

function nextLine() {
  response.value = ''
  if (currentIndex.value < currentScript.value.length - 1) {
    currentIndex.value++
  } else {
    if (part.value === 0) {
      lastSpeaker.value = currentLine.value?.name || ''
      isUserTurn.value = true
    } else {
      goNext()
    }
  }
}

function goNext() {
  if (game.meetingTime === 1) {
    game.nextScene = 'pas'
    game.goTo(game.nextScene)
  }
  else {
    game.currentVideo = 'intro2'
    game.nextScene = 'quiz'
    game.goTo('intro')
  }

}
</script>

<style scoped>
.meeting-scene {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.background {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>