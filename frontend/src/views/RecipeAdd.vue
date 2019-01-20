<template>
  <recipe-edit-form :recipe="recipe" @input="onUpdate" />
</template>

<script>
import RecipeEditForm from '@/components/RecipeEditForm'

export default {
  components: {
    RecipeEditForm,
  },
  data () {
    return {
      recipe: {}
    }
  },
  methods: {
    onUpdate (v) {
      this.recipe = v
      this.$router.push({
        name: 'recipe-detail',
        params: {
          id: this.recipe.id,
        }
      })
    }
  }
}
</script>
