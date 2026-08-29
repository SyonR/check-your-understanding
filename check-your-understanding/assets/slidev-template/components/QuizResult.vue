<template>
  <div v-if="results.length === total" class="quiz-result" :class="passed ? 'passed' : 'failed'">
    <div class="score-header">
      <h2 class="score-text">{{ correctCount }} / {{ total }} correct ({{ scorePercent }}%)</h2>
      <p class="verdict">
        {{ passed ? 'You passed! Great understanding of the codebase.' : 'Not quite — review the slides below and try again.' }}
      </p>
    </div>
    <div v-if="!passed && failedRefs.length" class="review-list">
      <h3>Slides to review:</h3>
      <ul>
        <li v-for="slideRef in failedRefs" :key="slideRef">
          Review: <strong>{{ slideRef }}</strong>
        </li>
      </ul>
    </div>
  </div>
  <div v-else class="quiz-result pending">
    <p class="pending-text">Answer all {{ total }} questions to see your result.</p>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
    </div>
    <p class="progress-label">{{ results.length }} / {{ total }} answered</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface QuizAnswer {
  id: string
  correct: boolean
  slide_ref?: string
}

const props = defineProps<{
  results: QuizAnswer[]
  total: number
  passThreshold: number
  slideRefs?: Record<string, string>
}>()

const correctCount = computed(() => props.results.filter(result => result.correct).length)
const scorePercent = computed(() => Math.round((correctCount.value / props.total) * 100))
const passed = computed(() => scorePercent.value / 100 >= props.passThreshold)
const progressPercent = computed(() => Math.round((props.results.length / props.total) * 100))

const failedRefs = computed(() =>
  props.results
    .filter(result => !result.correct)
    .map(result => result.slide_ref || props.slideRefs?.[result.id] || result.id),
)
</script>

<style scoped>
.quiz-result {
  margin-top: 1.5rem;
  padding: 1.25rem;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
}

.quiz-result.passed {
  border-color: #16a34a;
  background: #f0fdf4;
}

.quiz-result.failed {
  border-color: #ea580c;
  background: #fff7ed;
}

.quiz-result.pending {
  border-color: #d1d5db;
  background: #f9fafb;
}

.score-header {
  text-align: center;
}

.score-text {
  margin: 0.25rem 0;
  font-size: 1.4rem;
  font-weight: 700;
}

.verdict {
  color: #374151;
  font-size: 0.95rem;
}

.review-list {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.review-list h3 {
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
}

.review-list ul {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0;
  list-style: none;
}

.review-list li {
  color: #374151;
  font-size: 0.9rem;
}

.pending-text {
  margin-bottom: 0.75rem;
  color: #6b7280;
  font-size: 0.9rem;
  text-align: center;
}

.progress-bar {
  height: 8px;
  overflow: hidden;
  border-radius: 4px;
  background: #e5e7eb;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.progress-label {
  margin-top: 0.4rem;
  color: #9ca3af;
  font-size: 0.8rem;
  text-align: center;
}
</style>
