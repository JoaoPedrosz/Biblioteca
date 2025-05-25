import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import '@/assets/css/global.css'

// 1️⃣ Defina a URL base do seu backend Flask
axios.defaults.baseURL = 'http://localhost:5000'

// 2️⃣ Se já tiver token salvo, coloque no header
const token = localStorage.getItem('access_token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// 3️⃣ Injete o axios no Vue (para usar em this.$axios)
Vue.prototype.$axios = axios

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
