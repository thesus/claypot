<template>
  <div v-if="loading">
    {{ $t('home.loading') }}
  </div>
  <RecipeTableView
    v-else-if="!!recipes"
    :recipes="recipes"
    class="recipes"
  />
  <div v-else-if="!error && recipes.length === 0">
    {{ $t('home.no_recipes') }}
  </div>
  <div v-else-if="error">
    <div>{{ error }}</div>
    <div>
      <button @click="update">
        {{ $t('home.retry') }}
      </button>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import { mapGetters } from 'vuex'

import RecipeTableView from '@/components/RecipeTableView'

import { api, endpoints } from '@/api'

export default {
  name: 'RecipeList',
  components: {
    RecipeTableView,
  },
  props: {
    filters: {
      type: Object,
      default: () => ({}),
    },
  },
  data () {
    return {
      recipes: [],
      loading: false,
      error: '',
    }
  },
  watch: {
    filters () {
      this.update()
    },
  },
  mounted () {
    this.update()
  },
  methods: {
    async update () {
      try {
        this.loading = true
        const r = await api(endpoints.fetch_recipes(), this.filters, {method: 'GET'})
        if (r.ok) {
          this.recipes = await r.json()
          this.error = ''
        } else {
          throw new Error(this.$t('home.error'))
        }
      } catch (err) {
        this.error = err.message
        this.recipes.length = 0
      } finally {
        this.loading = false
      }
    },
    addRecipe () {
      this.$router.push({
        'name': 'recipe-add'
      })
    },
    showAllRecipes () {
      Vue.set(this, 'filters', {})
    },
    showMyFavorites () {
      Vue.set(this, 'filters', {is_starred: 2})
    },
    showMyRecipes () {
      Vue.set(this, 'filters', {is_my_recipe: 2})
    },
  },
}
</script>

<style lang="scss" scoped>
.recipes {
  padding: 5px;
}
</style>
