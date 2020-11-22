<template>
  <div>
    {{ $t('logout.message') }}
    <router-link :to="{ name: 'home' }">
      {{ $t('logout.home') }}
    </router-link>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  mounted() {
    this.$store.dispatch('logout')
    this.updateTitle({name: "titles.accounts.logout"})
  },
  methods: {
    ...mapActions(["updateTitle"]),
  },
}
</script>
