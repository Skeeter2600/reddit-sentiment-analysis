<script setup lang="ts">
import { ref } from 'vue';
import { API } from 'aws-amplify';
import type { Post } from '@/models/post.model';

const topic = ref('');
const subreddit = ref('');
const posts = ref<Post[]>([]);

async function get() {
  try {
    const response = await API.get('RedditSentimentAPI', '/posts', {
      queryStringParameters: {
        topic: topic.value,
        subreddit: subreddit.value
      }
    });

    posts.value = response as Post[];

    console.log(response);
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <label>Topic:</label>
  <input v-model="topic" />

  <label>Subreddit:</label>
  <input v-model="subreddit" />

  <button @click="get">Get Posts</button>
  <ul>
    <div v-for="post in posts" :key="post.postId">
      <h2>{{ post.title }}</h2>
      <p>{{ post.sentiment }}</p>
    </div>
  </ul>
</template>
