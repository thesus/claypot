<template>
  <RecipeEditForm
    @input="onUpdate"
  />
</template>

<script>
import RecipeEditForm from '@/components/RecipeEditForm'

export default {
  components: {
    RecipeEditForm,
  },
  methods: {
    onUpdate (v) {
      this.$router.push({
        name: 'recipe-detail',
        params: {
          id: v.id,
        }
      })
    }
  }
}
</script>
