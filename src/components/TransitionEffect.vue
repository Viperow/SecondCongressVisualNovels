<template>
  <div v-if="visible" class="transition-overlay" :class="effectClass" @animationend="onEnd"></div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{ effect: 'zoom' | 'swirl' | 'bubble' }>()
const emit = defineEmits(['end'])

const visible = ref(true)

const effectClass = computed(() => `effect-${props.effect}`)

function onEnd() {
  visible.value = false
  emit('end')
}
</script>

<style scoped>
.transition-overlay {
  position: fixed;
  inset: 0;
  background: black;
  z-index: 100;
}

.effect-zoom {
  animation: zoomInOut 1s forwards;
}
@keyframes zoomInOut {
  0% { transform: scale(0); border-radius: 50%; }
  100% { transform: scale(20); }
}
</style>