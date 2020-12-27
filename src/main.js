import Vue from 'vue'
import App from './App.vue'
import VueNativeSock from 'vue-native-websocket'

Vue.config.productionTip = false

Vue.use(VueNativeSock, 'ws://localhost:8765', {
  format: 'json',
  reconnection: true,
})

new Vue({
  render: h => h(App),
}).$mount('#app')
