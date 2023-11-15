<script lang="ts" setup>
import { ref } from 'vue';

const subreddits = ref([
  {
    name: 'rit'
  },
  {
    name: 'all'
  },
  {
    name: 'tf2'
  }
]);

function addSubreddit() {
  const name = prompt('subreddit name:');
  if (name) {
    subreddits.value.push({ name });
  }
}
</script>

<template>
  <div class="content">
    <ul>
      <li v-for="subreddit in subreddits" :key="subreddit.name">
        <RouterLink :to="`/r/${subreddit.name}`">r/{{ subreddit.name }}</RouterLink>
      </li>

      <li>
        <button @click="addSubreddit">+</button>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.content {
  ul li {
    list-style-type: none;

    a,
    button {
      border: none;
      background-color: transparent;
      cursor: pointer;
      color: white;
      text-decoration: none;

      display: flex;
      width: 100%;
      height: 40px;
      align-items: center;
      padding: 0 16px;

      transition: background-color 0.2s;
      transition: color 0.2s;

      &:hover {
        background-color: white;
        color: rgb(3, 144, 252);
      }
    }
  }
}
</style>
