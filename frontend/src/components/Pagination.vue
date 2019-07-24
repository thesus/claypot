<template>
  <div class="pagination">
    <button
      class="btn"
      :disabled="!previous"
      @click="$emit('update', previous)"
    >
      {{ $t('home.previous') }}
    </button>
    <button
      class="btn"
      :disabled="!next"
      @click="$emit('update', next)"
    >
      {{ $t('home.next') }}
    </button>
  </div>
</template>

<script>

export default {
  props: {
    next: {
      type: Number,
      default: null
    },
    previous: {
      type: Number,
      default: null
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

</style>
