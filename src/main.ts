import './assets/main.css'
import '@aws-amplify/ui-vue/styles.css';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { Amplify } from 'aws-amplify'
import awsExports from './aws-exports'
Amplify.configure(awsExports)

const app = createApp(App)

app.use(router)

app.mount('#app')
