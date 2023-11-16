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
// Needed for kendo charts
import 'hammerjs';

const props = defineProps<{
  topic: Topic;
}>();

const posts = ref<Post[]>(
  await API.get('RedditSentimentAPI', '/posts', {
    queryStringParameters: {
      topic: props.topic.topic,
      subreddit: props.topic.subreddit
    }
  })
);

function getSentimentString(sentiment: string | undefined): string {
  const lower = sentiment?.toLowerCase() ?? 'unknown';
  return lower[0].toUpperCase() + lower.substring(1);
}

function analyzeSentiments(): { [key: string]: number } {
  const sentiments: { [key: string]: number } = {};

  for (const post of posts.value) {
    console.log(post.sentiment);
    const sentiment = getSentimentString(post.sentiment);
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
  title: `${x.title} (${getSentimentString(x.sentiment)})`,
  content: x.title
}));

const sentiments = analyzeSentiments();
const pieData = Object.keys(sentiments).map((sentiment) => ({
  category: sentiment,
  value: sentiments[sentiment]
}));
</script>

<template>
  <div v-if="posts.length === 0">
    <h2>No posts matching this topic yet, check back later!</h2>
  </div>
  <div v-else>
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
  </div>
</template>

<style>
.k-animation-container.k-animation-container-relative.k-fade-enter-active {
  width: 100%;
}

.wrapper {
  padding: 10px;
}
</style>
