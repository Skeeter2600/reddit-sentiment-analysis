<script lang="ts" setup>
import type { Topic } from '@/models/topic.model';
import { useAuthenticator } from '@aws-amplify/ui-vue';
import { API, Auth } from 'aws-amplify';
import { ref } from 'vue';
import { Dialog, DialogActionsBar } from '@progress/kendo-vue-dialogs';
import { Button } from '@progress/kendo-vue-buttons';

const auth = useAuthenticator();

const subreddits = ref<string[]>([]);

try {
  await Auth.currentAuthenticatedUser();

  const subredditSet = new Set<string>();

  for (const sub of (
    await API.get('RedditSentimentAPI', '/topics', {
      queryStringParameters: {
        email: auth.user.attributes.email
      }
    })
  ).map((x: Topic) => x.subreddit)) {
    subredditSet.add(sub);
  }

  for (const sub of subredditSet) {
    subreddits.value.push(sub);
  }
} catch (ex) {
  console.error(ex);
}

const subredditTyped = ref('');
const topic = ref('');
const error = ref('');
const addingSubreddit = ref(false);

async function addSubreddit() {
  if (!auth?.user?.attributes?.email) {
    error.value = 'Must be logged in to use this!';
    return;
  }

  const subreddit = subredditTyped.value.trim().toLowerCase();
  if (!subreddit) {
    error.value = 'Missing subreddit!';
    return;
  }

  if (subreddits.value.find((x) => x === subreddit)) {
    error.value = 'You already have that subreddit!';
    return;
  }

  const topicValue = topic.value.trim();
  if (!topicValue) {
    error.value = 'Missing topic!';
    return;
  }

  addingSubreddit.value = true;

  await API.post('RedditSentimentAPI', '/topics', {
    queryStringParameters: {
      email: auth.user.attributes.email,
      topic: topicValue,
      subreddit: subreddit
    }
  });

  await API.post('RedditSentimentAPI', '/posts', {
    queryStringParameters: {
      topic: topicValue,
      subreddit: subreddit,
      limit: 10
    }
  });

  addingSubreddit.value = false;
  addSubredditDialog.value = false;

  subreddits.value.push(subreddit);
}

const addSubredditDialog = ref(false);
function toggleDialog() {
  addSubredditDialog.value = !addSubredditDialog.value;
  topic.value = '';
  subredditTyped.value = '';
  error.value = '';
}
</script>

<template>
  <div class="content">
    <ul>
      <li v-for="subreddit in subreddits" :key="subreddit">
        <RouterLink :to="`/r/${subreddit}`">r/{{ subreddit }}</RouterLink>
      </li>

      <li>
        <button @click="toggleDialog">+</button>
      </li>
    </ul>
  </div>

  <Dialog v-if="addSubredditDialog" title="Add Subreddit" @close="toggleDialog">
    <label for="subreddit">Subreddit</label>
    <input type="text" v-model="subredditTyped" id="subreddit" />
    <label for="topic">Topic</label>
    <input type="text" v-model="topic" id="topic" />
    <p v-if="error" style="color: red">{{ error }}</p>
    <dialog-actions-bar>
      <Button @click="toggleDialog" :disabled="addingSubreddit">Cancel</Button>
      <Button @click="addSubreddit" :disabled="addingSubreddit">Add</Button>
    </dialog-actions-bar>
  </Dialog>
</template>

<style scoped lang="scss">
label {
  display: block;
}
input {
  padding: 4px 3px;
  min-width: 300px;
  margin: 5px;
}

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
