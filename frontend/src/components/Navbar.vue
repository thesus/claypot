<template>
  <div class="nav">
    <div class="mobile">
      <button
        class="btn right"
        @click="status = !status"
      >
        {{ $t('navbar.button') }}
      </button>
    </div>
    <div
      class="items"
      :class="{ hidden: status }"
      @click="status = true"
    >
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

      <router-link
        v-if="isSuperUser"
        :to="{ name: 'admin' }"
      >
        {{ $t('navbar.admin') }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      status: true
    }
  },
  computed: {
    ...mapGetters([
      'isLoggedIn',
      'isSuperUser'
    ]),
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

$border_color: #ddd;

.nav {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  background-color: #56799C;
  min-height: 40px;

  z-index: 1000;
}

.mobile {
  display: none;
}

.items {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: row;
}

@media screen and (max-width: 500px) {
  .mobile {
    display: block;
    float: right;
    width: 100%;
    height: 50px;
    border-bottom: solid 1px rgba(255, 255, 255, 0.8);
    box-sizing: border-box;

    .btn {
      margin: 0;
      height: 100%;
      border: none;
      border-radius: 0;
      padding: 0 20px 0 20px !important;

      &:hover {
        background-color: white;
        color: inherit;
      }

      &:focus {
        outline: none;
        border: 0;
      }

      /* Remove gray outline used for keyboard navigation in firefox */
      &::-moz-focus-inner {
        border: 0;
      }
    }
  }

  .items {
    flex-direction: column;
    overflow: hidden;
    height: auto;
  }

  .hidden {
    height: 0;
  }
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
