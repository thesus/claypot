import Vue from 'vue'

const state = {
  homeView: true
}

const getters = {
  getHomeView: state => !!state.homeView
}

const actions = {}

const mutations = {
  updateProfile(state, data) {
    for (let [key, value] of Object.entries(data)) {
      Vue.set(state, key, value)
    }
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
