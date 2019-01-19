<template>
  <div v-if="!recipes">{{ $t('home.loading') }}</div>
  <article v-else-if="!!recipes">
    <h1>{{ $t('home.all_recipes') }}</h1>
    <ul>
      <li v-for="item in recipes" :key="item.id">
        <recipe-link :recipe="item"/>
      </li>
    </ul>
  </article>
</template>

<script>
import RecipeLink from '@/components/RecipeLink'

import {api, endpoints} from '@/api'

export default {
  name: 'home',
  components: {
    RecipeLink
  },
  data () {
    return {
      recipes: []
    }
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
        } else {
          throw new Error("Display some kind of error")
        }
      } catch (err) {
        // TODO: Display some kind of error
        this.recipes.clear()
      }
    }
  }
}
</script>
