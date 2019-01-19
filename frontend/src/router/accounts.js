import Login from '../views/accounts/Login'
import Logout from '../views/accounts/Logout'

import ResetPassword from '../views/accounts/ResetPassword'
import ResetConfirmPassword from '../views/accounts/ResetConfirmPassword'

import store from '@/store'

export default [
  {
    path: '/accounts/login',
    name: 'login',
    component: Login,
    beforeEnter: (to, from, next) => {
      // If the user is logged in, send him to /
      if (store.getters.isLoggedIn) {
        next({ name: 'home' })
      } else {
        next()
      }
    }
  },
  {
    path: '/accounts/logout',
    name: 'logout',
    component: Logout
  },
  {
    path: '/accounts/reset',
    name: 'reset-password',
    component: ResetPassword
  },
  {
    path: '/accounts/reset/:uid/:token',
    name: 'reset-confirm-password',
    component: ResetConfirmPassword
  }
]
