<script setup lang="ts">
import { ref } from 'vue'
import { API } from 'aws-amplify'
import type { Post } from '@/models/post.model'

const email = ref('')
const topic = ref('')
const subreddit = ref('')
const posts = ref<Post[]>([])

async function get() {
  try {
    const response = await API.get('RedditSentimentAPI', '/topics', {
      queryStringParameters: {
        email: email.value,
        topic: topic.value,
        subreddit: subreddit.value
      }
    })

    console.log(response)
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <input v-model="email" />
  <input v-model="topic" />
  <input v-model="subreddit" />
  <button @click="get">Get Posts</button>
  <ul>
    <li v-for="post in posts" :key="post.postId">
      {{ post.title }}
    </li>
  </ul>
</template>
