<template>
  <div>
    {{ $t('logout.message') }}
    <router-link :to="{ name: 'home' }">{{ $t('logout.home') }}</router-link>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('logout')
  }
}
</script>
