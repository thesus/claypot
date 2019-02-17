<template>
  <article>
    <h1>{{ $t('home.all_recipes') }}</h1>
    <router-link
      v-if="isLoggedIn"
      :to="{name: 'recipe-add'}"
    >
      {{ $t('home.add') }}
    </router-link>
    <RecipeList :filters="filters" />
  </article>
</template>

<script>
import Vue from 'vue'
import { mapGetters } from 'vuex'

import RecipeList from '@/components/RecipeList'

import { api, endpoints } from '@/api'

export default {
  name: 'Home',
  components: {
    RecipeList,
  },
  props: {
    filters: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
  methods: {
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
  },
}
</script>
