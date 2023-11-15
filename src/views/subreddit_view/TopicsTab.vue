<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { TabStrip, type TabStripTabProperties } from '@progress/kendo-vue-layout';
import type { Topic } from '@/models/topic.model';
import { API } from 'aws-amplify';

const props = defineProps<{
  topic: Topic;
}>();

// Simulate network request

const posts = await API.get('RedditSentimentAPI', '/posts', {
  queryStringParameters: {
    topic: props.topic.topic,
    subreddit: props.topic.subreddit
  }
});
</script>

<template>
  {{ JSON.stringify(posts) }}
</template>

<style scoped></style>
