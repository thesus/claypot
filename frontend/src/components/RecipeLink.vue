<template>
  <router-link :to="to">{{ title }}</router-link>
</template>

<script>
export default {
  name: 'RecipeLink',
  props: {
    recipe: {
      type: Object,
      default: () => ({}),
    },
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
