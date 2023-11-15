<script async setup lang="ts">
import { onMounted, ref } from 'vue';
import { TabStrip, type TabStripTabProperties } from '@progress/kendo-vue-layout';
import type { Topic } from '@/models/topic.model';

import TopicsTab from './TopicsTab.vue';

const props = defineProps<{ subreddit: string }>();

onMounted(() => {
  document.title = 'r/' + props.subreddit;
});

const selected = ref(0);
function onSelect(e: { selected: number }) {
  selected.value = e.selected;
}

// Simulate network request

const topics = ref(
  await new Promise<Topic[]>((resolve) => {
    setTimeout(() => {
      resolve([
        {
          topic: 'Topic A',
          subreddit: props.subreddit
        },
        {
          topic: 'Topic B',
          subreddit: props.subreddit
        }
      ]);
    }, 1000);
  })
);

const tabs = ref<TabStripTabProperties[]>(
  topics.value.map((x) => ({
    title: x.topic,
    content: x.topic
  }))
);
</script>

<template>
  <h2>r/{{ subreddit }}</h2>
  <TabStrip :selected="selected" @select="onSelect" :tabs="tabs">
    <template v-for="topic in topics" v-slot:[topic.topic] :key="topic.topic">
      <TopicsTab :topic="topic" />
    </template>
  </TabStrip>
</template>

<style scoped>
h2 {
  font-weight: 500;
  font-size: 2.6rem;
}
</style>
