<template>
  <input
    :value="value"
    :type="type"
    :placeholder="placeholder"
    @input="update"
  >
</template>

<script>
export default {
  props: {
    value: {
      type: [Object, String],
      required: true,
    },
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String,
      default: '',
    },
  },
  data () {
    return {
      debounce: null
    }
  },
  methods: {
    update(e) {
      clearTimeout(this.debounce)
      this.debounce = setTimeout(() => {
        this.$emit('input', e.target.value)
      }, 600)
    }
  }
}
</script>
