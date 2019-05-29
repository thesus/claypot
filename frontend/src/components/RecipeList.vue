<template>
  <div v-if="loading">
    {{ $t('home.loading') }}
  </div>
  <div v-else-if="!!recipes">
    <RecipeTableView
      :recipes="recipes"
      class="recipes"
    />

    <button class="btn" :disabled="!previous" @click="updateLink(previous)">{{ $t('home.previous') }}</button>
    <button class="btn" :disabled="!next" @click="updateLink(next)">{{ $t('home.next') }}</button>
  </div>
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
      next: null,
      previous: null,
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
    updateLink(url) {
      let page = url.searchParams.get('page')
      page = page ? page : 1
      this.$set(this, 'filters', {...this.filters, page: page})
    },
    async update () {
      /* Request format
      {
        count: 5,
        next: 3,
        previous: 1,
        results: [
          { id: 1, title: 'pie' }
        ]
      }
      */
      try {
        this.loading = true
        const r = await api(endpoints.fetch_recipes(), this.filters, {method: 'GET'})
        if (r.ok) {
          const result = await r.json()
          this.recipes = result['results']

          this.next = result['next'] === null ? null : new URL(result['next'])
          this.previous = result['previous'] === null ? null : new URL(result['previous'])

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
@import '@/modules/inputs.scss';

.recipes {
  padding: 5px;
}

.btn {
  margin: 3px;
}
</style>
