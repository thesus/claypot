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
    margin: 5px 5px 5px 5px;
    // border-bottom: solid 1px $border_color;
    // border-top: solid 1px $border_color;
}

a {
    margin: 8px 5px 5px 5px;
    display: inline-block;
    color: #2c3e50;
    text-decoration: none;
}

.router-link-exact-active {
    text-decoration: underline;
}
</style>
