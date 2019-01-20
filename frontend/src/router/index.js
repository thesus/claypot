import Vue from 'vue'
import Router from 'vue-router'

import Home from '../views/Home.vue'
import RecipeAdd from '../views/RecipeAdd.vue'
import RecipeDetail from '../views/RecipeDetail.vue'
import RecipeEdit from '../views/RecipeEdit.vue'

Vue.use(Router)

import accounts from './accounts'

export default new Router({
  mode: process.env.ROUTER_MODE || 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/recipes/add',
      name: 'recipe-add',
      component: RecipeAdd
    },
    {
      path: '/recipes/:id',
      name: 'recipe-detail',
      component: RecipeDetail
    },
    {
      path: '/recipes/:id/edit',
      name: 'recipe-edit',
      component: RecipeEdit
    },
    ...accounts
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/About.vue')
    // }i
  ]
})
