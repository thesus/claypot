<template>
  <span>{{ displayedValue }}</span>
</template>

<script>
export default {
  name: 'duration-span',
  props: {
    value: {
      type: String,
      default: '',
    }
  },
  computed: {
    displayedValue () {
      if (!this.value) {
        return ''
      }
      const parts = this.value.split(':')
      const hourPart = Number(parts[0])
      const minutePart = Number(parts[1])
      const secondPart = Number(parts[2])
      return `${hourPart}h ${minutePart}m`
    },
  },
}
</script>
