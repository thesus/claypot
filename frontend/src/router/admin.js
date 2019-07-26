import Admin from '../views/admin/Admin.vue'

import IngredientEdit from '../views/admin/IngredientEdit.vue'
import IngredientList from '../views/admin/IngredientList.vue'

export default [
  {
    path: '/admin',
    name: 'admin',
    component: Admin,
  },
  {
    path: '/admin/ingredients',
    name: 'ingredient-list',
    component: IngredientList,
  },
  {
    path: '/admin/ingredients/:id/edit',
    name: 'ingredient-edit',
    component: IngredientEdit,
  },
]
