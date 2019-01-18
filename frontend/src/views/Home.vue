<template>
  <div v-if="!recipes">Loading</div>
  <ul v-else-if="!!recipes">
    <li v-for="item in recipes" :key="item.id">
      <recipe-link :recipe="item"/>
    </li>
  </ul>
</template>

<script>
import RecipeLink from '@/components/RecipeLink'

import api from '@/api'

export default {
  name: 'home',
  components: {
    RecipeLink
  },
  data () {
    return {
      recipes: [
        {
          id: 1,
          title: "Test"
        }
      ]
    }
  },
  mounted () {
    this.update()
  },
  methods: {
    async update () {
      try {
        const r = await api('fetch_recipes')
        if (r.ok) {
          this.recipes = await r.json()
        } else {
          throw Error("Display some kind of error")
        }
      } catch (err) {
        // TODO: Display some kind of error
        this.recipes.clear()
      }
    }
  }
}
</script>
