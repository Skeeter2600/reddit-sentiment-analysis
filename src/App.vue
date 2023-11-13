<script setup lang="ts">
import SubredditBar from './components/SubredditBar.vue'
import { Authenticator } from '@aws-amplify/ui-vue'
import { Auth } from 'aws-amplify'

function goBack() {
  window.history.back()
}

function signOut() {
  try {
    Auth.signOut()
  } catch (error) {
    console.error(error)
  }
}
</script>

<template>
  <authenticator>
    <aside>
      <div class="bar">
        <button @click="goBack">&#x2190;</button>
      </div>

      <SubredditBar />
    </aside>
    <main>
      <header>
        <h1>Dashboard</h1>
        <button @click="signOut">Sign Out</button>
      </header>

      <RouterView />
    </main>
  </authenticator>
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
