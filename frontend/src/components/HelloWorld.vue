<script setup lang="ts">
import { ref, watch } from 'vue'
import debounce from 'lodash/debounce'

// defineProps<{

// }>()

const name = ref('')
const welcome = ref('')

const fetch_welcome = debounce(async (name: string) => {
  try {
    const response = await fetch('/api/v1/users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
      }),
      mode: 'cors',
      credentials: 'include',
    })
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }
    const result = await response.json()
    welcome.value = result.message
  } catch (error) {
    welcome.value = `Error: ${error}`
  }
}, 500)

watch(name, async (name) => {
  await fetch_welcome(name)
})
</script>

<template>
  <div>
    <div>Name input: <input v-model="name" /></div>
    <div>Name: {{ name }}</div>
    <div>Message: {{ welcome }}</div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
