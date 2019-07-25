<template>
  <div>
    <input
      :disabled="disabled"
      :value="displayedValue"
      @input="onInput"
    >
    <span>
      {{ $t('duration_input.minutes') }}
    </span>
  </div>
</template>

<script>
export default {
  name: 'DurationInput',
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

<style lang="scss" scoped>

div {
  width: 100%;
  position: relative;
}

/* Default input height is 30px */
/* on mobile devices 40px */
span {
  right: 6px;
  position: absolute;
  top: 4px;

  @media screen and (max-width: 500px) {
     top: 9px;
  }
}

input {
  width: 100%;
  padding-right: 65px;
  text-align: right;
}
</style>
