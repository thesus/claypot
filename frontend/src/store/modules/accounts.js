import router from '@/router'

import { api, endpoints } from '@/api'

const state = {
  user: null,
  loggedIn: false
}

const getters = {
  getUsername: state => state.user ? state.user.username : null,
  isLoggedIn: state => state.loggedIn,
}

const actions = {
  async login({ commit }, { username, password }) {
    try {
      const response = await api(
        endpoints.login(),
        {
          username: username,
          password: password
        }
      )

      if (response.ok) {
        commit(
          'login',
          {
            user: await response.json()
          }
        )
      } else {
        throw new Error()
      }
   } catch (err) {
      // TODO: Notification for errors
    }
  },
  logout({ commit }) {
    try {
      api(
        endpoints.logout()
      )
    } catch(err) {
      // This can fail silently.
    }

    commit('logout')
  }
}

const mutations = {
  login(state, { user }) {
    state.loggedIn = true
    state.user = user

    router.push({ 'path': router.currentRoute.query.next || '/' })
  },
  logout(state) {
    state.user = null
    state.loggedIn = false
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
