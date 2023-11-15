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

// Simulate network request

// {
//       "email": None, "topic": None, "subreddit": None
// }

/*
"paths": {
    "/topics": {
      "name": "/topics",
      "lambdaFunction": "TopicsAPILambda",
      "permissions": {
        "setting": "open"
      }
    },
    "/posts": {
      "name": "/posts",
      "lambdaFunction": "PostsAPILambda",
      "permissions": {
        "setting": "open"
      }
    },
    "/users": {
      "name": "/users",
      "lambdaFunction": "UsersAPILambda",
      "permissions": {
        "setting": "open"
      }
    }
  }
*/

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
    <label>Add a new topic for {{ subreddit }}</label>
    <p v-if="error" style="color: red">{{ error }}</p>
    <input type="text" @input="error = ''" v-model="topic" />
    <input type="submit" value="Add Topic" />
  </form>
</template>

<style scoped></style>
