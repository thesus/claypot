<template>
  <div v-if="!recipes">{{ $t('home.loading') }}</div>
  <article v-else-if="!!recipes">
    <h1>{{ $t('home.all_recipes') }}</h1>
    <router-link
      v-if="isLoggedIn"
      :to="{name: 'recipe-add'}">{{ $t('home.add') }}</router-link>
    <component
      :is="'RecipeTableView'"
      :recipes="recipes"
      class="recipes"/>
    <div v-if="!error && recipes.length === 0">{{ $t('home.no_recipes') }}</div>
    <div v-if="error">
      <div>{{ error }}</div>
      <div><button @click="update">{{ $t('home.retry') }}</button></div>
    </div>
  </article>
</template>

<script>
import { mapGetters } from 'vuex'

import RecipeLink from '@/components/RecipeLink'
import RecipeTableView from '@/components/RecipeTableView'

import { api, endpoints } from '@/api'

export default {
  name: 'Home',
  components: {
    RecipeLink,
    RecipeTableView,
  },
  data () {
    return {
      recipes: [],
      error: ''
    }
  },
  computed: {
    ...mapGetters([
      'isLoggedIn',
    ]),
  },
  mounted () {
    this.update()
  },
  methods: {
    async update () {
      try {
        const r = await api(endpoints.fetch_recipes())
        if (r.ok) {
          this.recipes = await r.json()
          this.error = ''
        } else {
          throw new Error(this.$t('home.error'))
        }
      } catch (err) {
        this.error = err.message
        this.recipes.length = 0
      }
    },
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
  }
}
</script>

<style lang="scss" scopd>
.recipes {
  padding: 5px;
}
</style>
