<script setup lang="ts">
import { ref } from 'vue';
import type { Topic } from '@/models/topic.model';
import { API } from 'aws-amplify';
import type { Post } from '@/models/post.model';
import { PanelBar } from '@progress/kendo-vue-layout';
import {
  Chart,
  ChartLegend,
  ChartSeries,
  ChartSeriesItem,
  ChartTitle
} from '@progress/kendo-vue-charts';
import 'hammerjs';

const props = defineProps<{
  topic: Topic;
}>();

// Simulate network request

const posts = ref<Post[]>(
  await API.get('RedditSentimentAPI', '/posts', {
    queryStringParameters: {
      topic: props.topic.topic,
      subreddit: props.topic.subreddit
    }
  })
);

if (posts.value.length === 0) {
  // Fill with fake posts for debug
  posts.value = [
    {
      postId: '123',
      subreddit: 'asdf',
      text: 'What a cool sample post!\nWow this is so cool!',
      title: 'Test post!',
      topics: [],
      sentiment: 'Positive'
    },
    {
      postId: '124',
      subreddit: 'asdf',
      text: 'Super duper angry!',
      title: 'Mad post!',
      topics: [],
      sentiment: 'Negative'
    },
    {
      postId: '12',
      subreddit: 'asdf',
      text: 'Oooo spooky!',
      title: 'Unknown post!',
      topics: [],
      sentiment: undefined
    }
  ];
}

function analyzeSentiments(): { [key: string]: number } {
  const sentiments: { [key: string]: number } = {};

  for (const post of posts.value) {
    const sentiment = post.sentiment ?? 'Unknown';
    if (sentiment) {
      if (!sentiments[sentiment]) {
        sentiments[sentiment] = 0;
      }

      sentiments[sentiment]++;
    }
  }

  return sentiments;
}

const items = posts.value.map((x) => ({
  title: `${x.title} (${x.sentiment ?? 'Unknown'})`,
  content: x.title
}));

const sentiments = analyzeSentiments();
const pieData = Object.keys(sentiments).map((sentiment) => ({
  category: sentiment,
  value: sentiments[sentiment]
}));
</script>

<template>
  <h2>Analysis</h2>

  <Chart>
    <ChartTitle text="Sentiment Analysis" />
    <ChartLegend :position="'bottom'" />
    <ChartSeries>
      <ChartSeriesItem
        :type="'pie'"
        :data-items="pieData"
        :field="'value'"
        :category-field="'category'"
        :labels="{ visible: true }"
      />
    </ChartSeries>
  </Chart>

  <h2>All posts</h2>

  <PanelBar expand-mode="multiple" :items="items">
    <template v-for="post in posts" v-slot:[post.title] :key="post.title">
      <div class="wrapper">
        <p v-for="text in post.text.split('\n')" :key="text">
          {{ text }}
        </p>
      </div>
    </template>
  </PanelBar>
</template>

<style>
.k-animation-container.k-animation-container-relative.k-fade-enter-active {
  width: 100%;
}

.wrapper {
  padding: 10px;
}
</style>
