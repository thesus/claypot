<template>
  <span>
    <input
      class=""
      :disabled="disabled"
      :value="displayedValue"
      @input="onInput"
    />&nbsp;{{ $t('duration_input.minutes') }}
  </span>
</template>

<script>
export default {
  name: 'duration-input',
  props: {
    value: {
      type: String,
      default: null,
    },
    disabled: {
      type: Boolean,
      default: false,
    }
  },
  computed: {
    displayedValue () {
      if ((typeof this.value === 'undefined') || (this.value === null) || this.value === '') {
        return ''
      }
      const parts = this.value.split(':')
      // second-part is ignored.
      const hourPart = Number(parts[0])
      const minutePart = Number(parts[1])
      return String(hourPart * 60 + minutePart)
    },
  },
  methods: {
    onInput (event) {
      const str = event.target.value
      if (str === '') {
        this.$emit('input', null)
        return
      }
      const num = Number(str)
      if (!isNaN(num)) {
        const hourPart = Math.floor(num / 60)
        const minutePart = num % 60
        this.$emit('input', `${(hourPart < 10 ? '0' : '') + String(hourPart)}:${(minutePart < 10 ? '0' : '') + String(minutePart)}:00`)
      }
    }
  },
}
</script>
