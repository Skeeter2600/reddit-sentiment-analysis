<script setup lang="ts">
import { ref } from 'vue';
import type { Topic } from '@/models/topic.model';
import { API } from 'aws-amplify';
import { useAuthenticator } from '@aws-amplify/ui-vue';

const auth = useAuthenticator();

const props = defineProps<{
  subreddit: string;
  doneTopics: Topic[];
}>();

const emits = defineEmits<{
  (e: 'done', topic: Topic): void;
}>();

const topic = ref('');
const error = ref('');

async function submitTopic() {
  const value = topic.value.trim();
  if (value.length === 0) {
    error.value = 'Please enter a topic!';
    return;
  }

  if (props.doneTopics.find((x) => x.topic.toLowerCase() === value.toLowerCase())) {
    error.value = 'You already watch this topic!';
    return;
  }

  try {
    await API.post('RedditSentimentAPI', '/topics', {
      queryStringParameters: {
        email: auth.user.attributes.email,
        topic: value,
        subreddit: props.subreddit
      }
    });

    emits('done', {
      subreddit: props.subreddit,
      topic: value
    });
  } catch (ex) {
    console.error(ex);
    alert('Something went wrong - see console');
  }
}
</script>

<template>
  <form action="" @submit.prevent="submitTopic">
    <label for="topic">Add a new topic for r/{{ subreddit }}</label>
    <input
      type="text"
      placeholder="Your awesome topic"
      id="topic"
      @input="error = ''"
      v-model="topic"
    />
    <p v-if="error" style="color: red">{{ error }}</p>
    <input type="submit" value="Add Topic" />
  </form>
</template>

<style scoped lang="scss">
label {
  display: block;
  font-size: 1.4em;
}
input {
  display: block;
  padding: 4px 3px;
  min-width: 300px;
  margin: 10px;
}
input[type='submit'] {
  border: none;
  padding: 8px 6px;
  cursor: pointer;
  background-color: rgb(3, 144, 252);
  color: white;

  &:hover {
    background-color: white;
    color: rgb(3, 144, 252);
    outline: thin solid rgb(3, 144, 252);
  }
}
</style>
