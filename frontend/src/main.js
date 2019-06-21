import Vue from 'vue'

import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';

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
        Sentry.init({
          dsn: config.sentry_dsn,
          integrations: [new Integrations.Vue({Vue, attachProps: true})],
        });
      }
    } else {
      throw new Error('Sentry setup failed', r)
    }
  } catch (err) {
    console.log('Sentry setup failed')
  }
})()
