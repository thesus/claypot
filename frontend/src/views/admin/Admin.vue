<template>
  <router-link
    :to="{ name: 'ingredient-list' }"
  >
    Ingredient Edit
  </router-link>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  mounted () {
    this.updateTitle({name: "titles.admin.admin"})
  },
  methods: {
    ...mapActions(["updateTitle"]),
  },
}
</script>
