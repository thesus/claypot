<template>
  <router-link :to=to>{{ title }}</router-link>
</template>

<script>
export default {
  name: 'recipe-link',
  props: {
    recipe: Object
  },
  computed: {
    title () {
      return this.recipe.title
    },
    to () {
      return {
        name: 'recipe-detail',
        params: {
          id: this.recipe.id
        }
      }
    }
  }
}
</script>
