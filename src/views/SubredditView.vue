<script async setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import SubredditView from './subreddit_view/SubredditView.vue';

const route = useRoute();

const subreddit = ref(route.params.subreddit as string);

watch(
  () => route.params.subreddit,
  (newSubreddit) => {
    subreddit.value = newSubreddit as string;
  }
);
</script>

<template>
  <Suspense :key="subreddit">
    <SubredditView :subreddit="subreddit" />

    <template #fallback> <h2>Loading...</h2></template>
  </Suspense>
</template>

<style scoped>
h2 {
  font-weight: 500;
  font-size: 2.6rem;
}
</style>
