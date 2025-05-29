// src/stores/puzzle.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePuzzleStore = defineStore('puzzle', () => {
  // 存储密码答案的状态
  const correctAnswer = ref('')
  
  // 设置密码的方法
  const setCorrectAnswer = (answer: string) => {
    correctAnswer.value = answer
    console.log('密码已设置:', answer) // 调试用
  }
  
  // 检查密码是否正确的方法
  const checkAnswer = (input: string) => {
    return input === correctAnswer.value
  }

  return {
    correctAnswer,
    setCorrectAnswer,
    checkAnswer
  }
})