<template>
  <div class="nav">
    <router-link :to="{ name: 'home' }">
      {{ $t('navbar.home') }}
    </router-link>
    <router-link
      v-if="isLoggedIn"
      :to="{name: 'recipe-favorites'}"
    >
      {{ $t('navbar.my_favorites') }}
    </router-link>
    <router-link
      v-if="isLoggedIn"
      :to="{name: 'recipe-my-recipes'}"
    >
      {{ $t('navbar.my_recipes') }}
    </router-link>
    <router-link
      v-if="isLoggedIn"
      :to="{ name: 'logout' }"
    >
      {{ $t('navbar.logout') }}
    </router-link>
    <router-link
      v-if="!isLoggedIn"
      :to="{ name: 'login' }"
    >
      {{ $t('navbar.login') }}
    </router-link>
    <router-link
      v-if="!isLoggedIn"
      :to="{ name: 'signup' }"
    >
      {{ $t('navbar.signup') }}
    </router-link>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
}
</script>

<style lang="scss" scoped>
$border_color: #ddd;

.nav {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  background-color: #56799C;
}

a {
    padding: 10px 8px 8px 8px;
    display: inline-block;
    color: white;
    font-weight: bolder;
    text-decoration: none;
}

.router-link-exact-active {
   background-color: #0D5480;
}
</style>
