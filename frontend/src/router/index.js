import Vue from 'vue'
import Router from 'vue-router'

import Home from '../views/Home.vue'
import RecipeDetail from '../views/RecipeDetail.vue'
import RecipeEdit from '../views/RecipeEdit.vue'

import PageNotFound from '../views/PageNotFound.vue'

Vue.use(Router)

import accounts from './accounts'
import admin from './admin'

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/favorites',
      name: 'recipe-favorites',
      component: Home,
      props: {
        filters: {is_starred: 2},
        titleName: "titles.recipe-favorites",
      },
    },
    {
      path: '/my-recipes',
      name: 'recipe-my-recipes',
      component: Home,
      props: {
        filters: {is_my_recipe: 2},
        titleName: "titles.recipe-my-recipes",
      },
    },
    {
      path: '/recipes/add',
      name: 'recipe-add',
      component: RecipeEdit
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
    ...accounts,
    ...admin,
    {
      path: '*',
      component: PageNotFound
    }
  ]
})
