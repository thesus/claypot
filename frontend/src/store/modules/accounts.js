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

      console.log(response)
      commit(
        'login',
        {
          user: response
        }
      )
    } catch (err) {
      // TODO: Notification for errors
    }
  }
}

const mutations = {
  login(state, { user }) {
    state.loggedIn = true
    state.user = user

    router.push({ 'path': router.currentRoute.query.next || '/' })
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
