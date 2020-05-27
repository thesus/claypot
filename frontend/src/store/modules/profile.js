import Vue from 'vue'

const state = {
  homeView: true,
  extendedSearch: false,
}

const getters = {
  getHomeView: state => !!state.homeView,
  getExtendedSearch: state => !!state.extendedSearch
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
