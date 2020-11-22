import Vue from 'vue'

import App from './App.vue'

import router from './router'
import store from './store'
import i18n from './i18n'

// Old URL compatibility
const redirectActive = (function () {
  const oldLocation = window.location.hash.substring(1)
  if (oldLocation.length > 0 && oldLocation[0] === '/') {
    window.location.href = oldLocation
    return true
  }
  return false
})()

if (!redirectActive) {
  Vue.config.productionTip = false

  const vue = new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
  })
  vue.$mount('#app');
}
