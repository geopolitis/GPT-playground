import Vue from 'vue'
import App from './App.vue';
import './components/tailwind.css';

import Chatbot from './components/Chatbot.vue';
import Roles from './components/Roles.vue';
import AppHeader from './components/Header.vue';
Vue.component('AppHeader', AppHeader);

Vue.component('Chatbot', Chatbot);
Vue.component('Roles', Roles);

new Vue({
  render: h => h(App),
}).$mount('#app')