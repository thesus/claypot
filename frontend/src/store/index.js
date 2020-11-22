import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import accounts from './modules/accounts'
import htmlTitle from './modules/html-title'
import profile from './modules/profile'
import sentry from './modules/sentry'


import { api, endpoints } from '@/api'
import { getCookie } from '@/utils'

Vue.use(Vuex)



const store = new Vuex.Store({
  plugins: [
    createPersistedState({
      paths: ['accounts', 'profile'],
      getState(key, storage) {
        let value = storage.getItem(key)
        if (typeof value === 'undefined') {
          return undefined
        }
        try {
          value = JSON.parse(value)
        } catch (err) {
          value = undefined
        }
        if (typeof value === 'object' && value) {
          if (!value.accounts || !value.accounts.user || !value.accounts.user.pk) {
            delete value.loggedIn
            return value
          }
          (async function (pk) {
            try {
              const r = await api(endpoints.fetch_user(pk))
              if (r.ok) {
                store.commit('login', {user: await r.json()})
              } else {
                store.commit('logout')
              }
            } catch (err) {
              store.commit('logout')
            }
          })(value.accounts.user.pk)
        }
        return value
      },
    }),
  ],
  modules: {
    accounts,
    htmlTitle,
    profile,
    sentry,
  },
})

store.dispatch("assertSentryDsn")

export default store
