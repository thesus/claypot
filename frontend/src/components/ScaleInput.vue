<template>
  <span>
    <input v-model="numerator"/>
    <input v-model="denominator" v-if="!denominatorHidden"/>
    <button @click="increase">+</button>
    <button @click="decrease">-</button>
  </span>
</template>

<script>
export default {
  name: 'scale-input',
  data () {
    return {
      denominator: 1,
      numerator: 1,
      denominatorHidden: true,
    }
  },
  computed: {
    fraction () {
      const result = this.numerator / this.denominator
      if (!isNaN(result)) {
        return result
      } else {
        return 1.0
      }
    },
  },
  methods: {
    increase () {
      this.numerator += 1
    },
    decrease () {
      if (this.numerator - 1 === 0) {
        this.numerator = 1
        this.denominator += 1
        this.denominatorHidden = false
      } else {
        this.numerator -= 1
      }
    },
  },
  watch: {
    fraction () {
      this.$emit('input', this.fraction)
    }
  },
}
</script>
