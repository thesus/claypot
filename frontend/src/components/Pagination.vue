<template>
  <div class="pagination">
    <button
      class="btn"
      :disabled="!previous"
      @click="$emit('input', previous)"
    >
      {{ $t('home.previous') }}
    </button>
    <button
      class="btn"
      :disabled="!next"
      @click="$emit('input', next)"
    >
      {{ $t('home.next') }}
    </button>
  </div>
</template>

<script>

export default {
  props: {
    next: {
      type: String,
      default: null
    },
    previous: {
      type: String,
      default: null
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

</style>
