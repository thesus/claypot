import i18n from '@/i18n'

const state = {}
const getter = {}
const mutations = {}
const actions = {
  updateTitle (state, {name, args}) {
    const newTitle = i18n.t(name, args)
    document.title = newTitle
  }
}

export default {
  state,
  getter,
  mutations,
  actions,
}
