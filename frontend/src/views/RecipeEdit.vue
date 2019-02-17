<template>
  <div v-if="loading">
    {{ $t('recipe_edit.loading') }}
  </div>
  <div v-else-if="error">
    {{ $t('recipe_edit.loading_error') }}
  </div>
  <RecipeEditForm
    v-else-if="recipe"
    :recipe="recipe"
    @input="onUpdate"
  />
  <div v-else>
    {{ $t('recipe_edit.no_data') }}
  </div>
</template>

<script>
import {api, endpoints} from '@/api'
import RecipeEditForm from '@/components/RecipeEditForm'

export default {
  components: {
    RecipeEditForm,
  },
  data () {
    return {
      loading: false,
      error: false,
      recipe: {},
    }
  },
  computed: {
    recipeId () {
      return this.$route.params.id
    },
  },
  mounted () {
    this.update()
  },
  methods: {
    async update () {
      if (!this.recipeId) {
        return
      }
      try {
        this.loading = true
        const r = await api(endpoints.fetch_recipe(this.recipeId))
        this.loading = false
        if (r.ok) {
          this.recipe = await r.json()
        } else {
          throw new Error("Display some kind of error")
        }
      } catch (err) {
        // TODO: Display some kind of error
        this.error = true
      }
    },
    onUpdate () {
      this.$router.push({
        name: 'recipe-detail',
        params: {
          id: this.$route.params.id,
        },
      })
    }
  }
}
</script>
