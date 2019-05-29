<template>
  <input @input="update" :value="value" :type="type" :placeholder="placeholder">
</template>

<script>
export default {
  props: {
    value: {},
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String
    }
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
