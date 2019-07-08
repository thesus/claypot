import Admin from '../views/Admin.vue'

import IngredientEdit from '../views/IngredientEdit.vue'
import IngredientList from '../views/IngredientList.vue'

export default [
  {
    path: '/admin',
    name: 'admin',
    component: Admin
  },
  {
    path: '/admin/ingredients',
    name: 'ingredient-list',
    component: IngredientList
  },
  {
    path: '/admin/ingredients/:id/edit',
    name: 'ingredient-edit',
    component: IngredientEdit
  }
]
