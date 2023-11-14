<script setup lang="ts">
import SubredditBar from './components/SubredditBar.vue'
import { Authenticator, useAuthenticator } from '@aws-amplify/ui-vue'
import { ref } from 'vue'

const showAuthBox = ref(false)
const auth = useAuthenticator()

function goBack() {
  window.history.back()
}

function showAuthModal() {
  showAuthBox.value = true
}

function hideAuthModal() {
  showAuthBox.value = false
}
</script>

<template>
  <authenticator variation="modal" v-if="showAuthBox">
    <template v-slot:footer>
      <button @click="hideAuthModal()" style="width: 100%">CLOSE</button>
    </template>
  </authenticator>

  <aside>
    <div class="bar">
      <button @click="goBack">&#x2190;</button>
    </div>

    <SubredditBar />
  </aside>
  <main>
    <header>
      <h1>Dashboard</h1>
      <h3 v-if="auth.user?.username">{{ auth.user?.attributes.email }}</h3>
      <button v-if="auth.authStatus === 'authenticated'" @click="auth.signOut()">Sign Out</button>
      <button v-else @click="showAuthModal">Sign In</button>
    </header>

    <RouterView />
  </main>
</template>

<style lang="scss">
#app {
  flex-direction: row;
}

main {
  flex: 1;

  header {
    background-color: rgb(3, 144, 252);
    width: 100%;
    height: 50px;
    box-shadow: 0px 4px 5px 0px rgba(0, 0, 0, 0.22);
    color: white;
    display: flex;
    align-items: center;
    padding: 0 12px;

    h1 {
      font-weight: 400;
      font-size: 2em;
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
