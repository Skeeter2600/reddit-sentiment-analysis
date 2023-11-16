<script async setup lang="ts">
import { onMounted, ref } from 'vue';
import { TabStrip, type TabStripTabProperties } from '@progress/kendo-vue-layout';
import type { Topic } from '@/models/topic.model';

import AddNewTopic from './AddNewTopic.vue';
import TopicsTab from './TopicsTab.vue';
import { API } from 'aws-amplify';
import { useAuthenticator } from '@aws-amplify/ui-vue';

const auth = useAuthenticator();

if (!auth.user?.attributes?.email) {
  window.location.href = '/';
}

const props = defineProps<{ subreddit: string }>();

onMounted(() => {
  document.title = 'r/' + props.subreddit;
});

const selected = ref(0);
function onSelect(e: { selected: number }) {
  selected.value = e.selected;
}

// Simulate network request

// const topics = ref(
//   await new Promise<Topic[]>((resolve) => {
//     setTimeout(() => {
//       resolve([
//         {
//           topic: 'Topic A',
//           subreddit: props.subreddit
//         },
//         {
//           topic: 'Topic B',
//           subreddit: props.subreddit
//         }
//       ]);
//     }, 1000);
//   })
// );

const topics = ref<Topic[]>([]);

try {
  topics.value = await API.get('RedditSentimentAPI', '/topics', {
    queryStringParameters: {
      email: auth.user?.attributes?.email
    }
  });
} catch (ex) {
  console.error(ex);
  topics.value = [];
}

const tabs = ref<TabStripTabProperties[]>([
  ...topics.value.map((x) => ({
    title: x.topic,
    content: x.topic
  })),
  { title: 'Add New Topic', content: 'AddNewTopic' }
]);

function addNewTopic(topic: Topic) {
  topics.value.push(topic);

  // Add new tab before the "add new topic" tab
  const last = tabs.value.pop();
  tabs.value.push({ title: topic.topic, content: topic.topic });
  if (last) {
    tabs.value.push(last);
  }
}
</script>

<template>
  <h2>r/{{ subreddit }}</h2>
  <TabStrip :selected="selected" @select="onSelect" :tabs="tabs">
    <template v-for="topic in topics" v-slot:[topic.topic] :key="topic.topic">
      <Suspense>
        <TopicsTab :topic="topic" />

        <template #fallback>
          <p>Loading...</p>
        </template>
      </Suspense>
    </template>

    <template #AddNewTopic>
      <AddNewTopic @done="addNewTopic" :subreddit="subreddit" :doneTopics="topics" />
    </template>
  </TabStrip>
</template>

<style scoped>
h2 {
  font-weight: 500;
  font-size: 2.6rem;
}
</style>
