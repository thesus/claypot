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
      const result = Number(this.numerator) / Number(this.denominator)
      if (!isNaN(result)) {
        return result
      } else {
        return 1.0
      }
    },
  },
  methods: {
    increase () {
      if (!isNaN(Number(this.numerator))) {
        this.numerator = Number(this.numerator) + 1
      } else {
        this.numerator = 1
      }
    },
    decrease () {
      if (isNaN(Number(this.numerator)) || isNaN(Number(this.denominator))) {
        this.numerator = 1
        this.denominator = 1
        return
      }
      if (this.numerator - 1 === 0) {
        this.numerator = 1
        this.denominator = Number(this.denominator) + 1
        this.denominatorHidden = false
      } else {
        this.numerator = Number(this.numerator) - 1
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
