<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const subreddit = ref(route.params.subreddit as string);

function reloadValues() {
  document.title = 'r/' + subreddit.value;
}

watch(() => route.params.subreddit,
  newSubreddit => {
    subreddit.value = newSubreddit as string;
    reloadValues();
  }
);

onMounted(() => {
  reloadValues();
});

</script>

<template>
  <title>{{ subreddit }}</title>

  <div class="greetings">
    <h2>r/{{ subreddit }}</h2>
  </div>
</template>

<style scoped>
h2 {
  font-weight: 500;
  font-size: 2.6rem;
}
</style>
