<script setup lang="ts">
import SubredditBar from './components/SubredditBar.vue';
import { Authenticator, useAuthenticator } from '@aws-amplify/ui-vue';
import { ref } from 'vue';
import '@progress/kendo-theme-default/dist/all.css';

const showAuthBox = ref(false);
const auth = useAuthenticator();

function showAuthModal() {
  showAuthBox.value = true;
}

function hideAuthModal() {
  showAuthBox.value = false;
}

// If this value changes, the page will update all of its contents
const refresh = ref(0);

function signOut() {
  auth.signOut();
  refresh.value++;
}
</script>

<template>
  <Authenticator variation="modal" v-if="showAuthBox">
    <template v-slot:footer>
      <button @click="hideAuthModal()" style="width: 100%">CLOSE</button>
    </template>
  </Authenticator>

  <aside :key="refresh">
    <div class="bar">
      <h1>Subreddits</h1>
    </div>

    <Suspense>
      <SubredditBar />

      <template #fallback> Loading... </template>
    </Suspense>
  </aside>
  <main :key="refresh">
    <header>
      <h1>Dashboard</h1>
      <h3 v-if="auth.user?.username">{{ auth.user?.username }}</h3>
      <button v-if="auth.authStatus === 'authenticated'" @click="signOut">Sign Out</button>
      <button v-else @click="showAuthModal">Sign In</button>
    </header>

    <RouterView />
  </main>
</template>

<style lang="scss">
#app {
  flex-direction: row;
}

h1 {
  flex: 1;
  font-weight: 400;
  font-size: 2em;
}

h2 {
  flex: 1;
  font-weight: 400;
  font-size: 1.5em;
}

main {
  display: flex;
  flex-direction: column;
  flex: 1;

  header {
    background-color: rgb(3, 144, 252);
    width: 100%;
    height: 50px;
    box-shadow: 0px 4px 5px 0px rgba(0, 0, 0, 0.22);
    color: white;
    display: flex;
    align-items: center;
    padding: 0 0 0 12px;
    display: flex;
    flex-direction: row;

    button {
      padding: 0 20px;
      background-color: transparent;
      border: none;
      height: 100%;
      color: white;
      cursor: pointer;

      margin-left: 10px;

      &:hover {
        background-color: white;
        color: rgb(3, 144, 252);
      }
    }
  }
}

aside {
  color: white;
  width: 300px;
  background-color: #333;

  .bar {
    height: 50px;
    box-shadow: 0px 4px 5px 0px rgba(0, 0, 0, 0.22);
    margin-bottom: 10px;
    background-color: rgb(255, 150, 46);
    display: flex;

    button {
      background-color: transparent;
      border: none;
      color: white;
      font-size: 2em;
      display: flex;
      cursor: pointer;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      padding: 0 16px;

      &:hover {
        background-color: rgba(0, 0, 0, 0.1);
      }
    }
  }
}
</style>
