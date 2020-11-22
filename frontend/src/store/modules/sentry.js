import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';

import {api, endpoints} from '@/api'

const state = {
  dsn: null,
}

const getters = {}

const mutations = {
  setSentryDsn (state, {dsn}) {
    state.dsn = dsn
  },
}

const actions = {
  async assertSentryDsn({commit, state}) {
    if (state.dsn === "") {
      try {
        const r = await api(endpoints.fetch_sentry_config())
        if (r.ok) {
          const config = await r.json()
          commit("setSentryDsn", {dsn: config.sentry_dsn})
        } else {
          throw new Error('Sentry setup failed', r)
        }
      } catch (err) {
        console.log('Sentry setup failed', err)
      }
    }
    if (state.dsn) {
      Sentry.init({
        dsn: state.dsn,
        integrations: [new Integrations.Vue({Vue, attachProps: true})],
      });
    }
  },
}

export default {
  state,
  getters,
  mutations,
  actions,
}
