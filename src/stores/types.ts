// types.ts
export interface DialogueStep {
    type: 'text' | 'choice'
    content: string
    image?: string
    sound?: string
    effect?: 'confetti' | 'shake' | null
    options?: string[]
    answer?: number
    correctResponse?: string
    wrongResponse?: string
    correctImage?: string
    wrongImage?: string
    correctSound?: string
    wrongSound?: string
  }
  