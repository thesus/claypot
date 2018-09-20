import Vue from 'vue'
import Router from 'vue-router'

import Home from '../views/Home.vue'
import RecipeDetail from '../views/RecipeDetail.vue'

Vue.use(Router)

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
      path: '/recipes/:id',
      name: 'recipe-detail',
      component: RecipeDetail
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/About.vue')
    // }
  ]
})
