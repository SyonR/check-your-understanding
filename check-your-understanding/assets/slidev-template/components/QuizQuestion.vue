<template>
  <div class="quiz-question">
    <h3 class="prompt">{{ prompt }}</h3>
    <div class="options">
      <button
        v-for="(option, index) in options"
        :key="index"
        class="quiz-btn"
        :class="getButtonClass(option)"
        :disabled="answered"
        @click="selectAnswer(option)"
      >
        {{ option }}
      </button>
    </div>
    <div v-if="answered" class="rationale">
      <strong>{{ chosen === answer ? 'Correct!' : 'Incorrect.' }}</strong>
      {{ rationale }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  id: string
  type?: string
  prompt: string
  options: string[]
  answer: string
  rationale: string
}>()

const emit = defineEmits<{
  answered: [payload: { id: string; correct: boolean }]
}>()

const answered = ref(false)
const chosen = ref<string | null>(null)

function selectAnswer(option: string) {
  if (answered.value) return
  chosen.value = option
  answered.value = true
  emit('answered', { id: props.id, correct: option === props.answer })
}

function getButtonClass(option: string) {
  if (!answered.value) return ''
  if (option === props.answer) return 'correct'
  if (option === chosen.value) return 'wrong'
  return ''
}
</script>

<style scoped>
.quiz-question {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f7f8fa;
}

.prompt {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.quiz-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.15s;
}

.quiz-btn:hover:not(:disabled) {
  background: #eff6ff;
  border-color: #3b82f6;
}

.quiz-btn.correct {
  background: #dcfce7;
  border-color: #16a34a;
  color: #15803d;
}

.quiz-btn.wrong {
  background: #fee2e2;
  border-color: #dc2626;
  color: #b91c1c;
}

.quiz-btn:disabled {
  pointer-events: none;
}

.rationale {
  margin-top: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-left: 3px solid #6b7280;
  border-radius: 0 4px 4px 0;
  background: white;
  color: #374151;
  font-size: 0.85rem;
}

</style>
