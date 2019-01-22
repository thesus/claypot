<template>
  <div v-if="!recipes">{{ $t('home.loading') }}</div>
  <article v-else-if="!!recipes">
    <h1>{{ $t('home.all_recipes') }}</h1>
    <button v-if="isLoggedIn" @click="addRecipe">{{ $t('home.add') }}</button>
    <ul v-if="!error && recipes.length > 0">
      <li v-for="item in recipes" :key="item.id">
        <recipe-link :recipe="item"/>
      </li>
    </ul>
    <div v-if="!error && recipes.length === 0">{{ $t('home.no_recipes') }}</div>
    <div v-if="error">
      <div>{{ error }}</div>
      <div><button @click="update">{{ $t('home.retry') }}</button></div>
    </div>
  </article>
</template>

<script>
import {mapGetters} from 'vuex'

import RecipeLink from '@/components/RecipeLink'

import {api, endpoints} from '@/api'

export default {
  name: 'home',
  components: {
    RecipeLink
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
