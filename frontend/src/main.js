import Vue from 'vue'
import Raven from 'raven-js';
import RavenVue from 'raven-js/plugins/vue';

import App from './App.vue'

import router from './router'
import store from './store'
import i18n from './i18n'

import {api, endpoints} from '@/api'

(async function () {
  Vue.config.productionTip = false

  const vue = new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
  })
  vue.$mount('#app')

  try {
    const r = await api(endpoints.fetch_sentry_config())
    if (r.ok) {
      const config = await r.json()
      if (config.sentry_dsn) {
        Raven.config(config.sentry_dsn).addPlugin(RavenVue, vue).install()
      }
    } else {
      throw new Error('Sentry setup failed', r)
    }
  } catch (err) {
    console.log('Sentry setup failed')
  }
})()
