<template>
  <div>
    <div v-if="loading">
      {{ $t('recipe_edit.loading') }}
    </div>
    <div v-else-if="error">
      {{ $t('recipe_edit.loading_error') }}
    </div>

    <RecipeEditForm
      :id="recipeId"
      @update="onUpdate"
      @remove="onRemove"

      @loadingStart="onLoadingStart"
      @loadingEnd="onLoadingEnd"
      @error="error = true"
    />
  </div>
</template>

<script>
import {mapActions} from 'vuex'

import RecipeEditForm from '@/components/recipe-edit/RecipeEditForm'

export default {
  components: {
    RecipeEditForm,
  },
  props: {
    'onRemoveRouteTo': {
      type: Object,
      default: () => ({name: 'home'}),
    }
  },
  data () {
    return {
      loading: false,
      error: false,
      success: false,
      timer: null
    }
  },
  computed: {
    recipeId () {
      return this.$route.params.id ? Number.parseInt(this.$route.params.id, 10) : null
    },
  },
  methods: {
    onUpdate (id) {
      this.$router.push({
        name: 'recipe-detail',
        params: {
          id: id,
        },
      })
    },
    onRemove () {
      this.$router.push(this.onRemoveRouteTo)
    },
    onLoadingStart () {
      this.timer = setTimeout(() => { this.loading = true }, 200)
    },
    onLoadingEnd ({recipe}) {
      if (recipe !== null) {
        this.updateTitle({name: "titles.recipeEdit.ok", args: {title: recipe.title}})
      } else {
        this.updateTitle({name: "titles.recipeEdit.error"})
      }
      clearTimeout(this.timer)
      this.loading = false
      if (!this.error) {
        this.success = true
      }
    },
    ...mapActions(["updateTitle"]),
  },
}
</script>
