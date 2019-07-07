import Vue from 'vue'
import Router from 'vue-router'

import Home from '../views/Home.vue'
import RecipeAdd from '../views/RecipeAdd.vue'
import RecipeDetail from '../views/RecipeDetail.vue'
import RecipeEdit from '../views/RecipeEdit.vue'
import IngredientEdit from '../views/IngredientEdit.vue'
import IngredientList from '../views/IngredientList.vue'

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
      path: '/favorites',
      name: 'recipe-favorites',
      component: Home,
      props: {
        filters: {is_starred: 2},
      },
    },
    {
      path: '/my-recipes',
      name: 'recipe-my-recipes',
      component: Home,
      props: {
        filters: {is_my_recipe: 2},
      },
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
    {
      path: '/admin/ingredients/:id/edit',
      name: 'ingredient-edit',
      component: IngredientEdit
    },
    {
      path: '/admin/ingredients',
      name: 'ingredient-list',
      component: IngredientList
    },
    ...accounts
    // {
    //   path: '/about',
    //   name: 'about',
    //   component: () => import('../views/About.vue')
    // }i
  ]
})
