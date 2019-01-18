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
    update () {
      const data = await api('fetch_recipes')
      console.log(data)
    }
  }
}
</script>
