// import Vue from 'vue'
// import VueMoment from 'vue-moment'
import { createApp } from 'vue'
import App from './App.vue'
import router from "./router/index"
import './index.css'

// Vue.use(require(VueMoment));

createApp(App).use(router).mount('#app')
