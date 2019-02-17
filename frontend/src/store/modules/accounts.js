import router from '@/router'

import { api, endpoints, InvalidRequestError } from '@/api'

const state = {
  user: null,
  loggedIn: false
}

const getters = {
  getUsername: state => state.user ? state.user.username : null,
  isLoggedIn: state => state.loggedIn,
  isSuperUser: state => state.user ? state.user.is_superuser : false,
  userId: state => state.user ? state.user.pk : null,
}

const actions = {
  async login({ commit }, { username, password }) {
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

      router.push({ 'path': router.currentRoute.query.next || '/' })
    } else {
      throw new InvalidRequestError(
        response.status,
        await response.json()
      )
    }
  },
  async logout({ commit }) {
    try {
      await api(
        endpoints.logout(),
        null,
        {method: 'post'}
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
