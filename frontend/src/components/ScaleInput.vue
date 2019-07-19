<template>
  <div class="scale">
    <div
      class="button"
      @click="decrease"
    >
      -
    </div>
    <span v-if="denominatorHidden">{{ numerator }}</span>
    <span
      v-else
      class="fraction"
    >
      <sup>{{ numerator }}</sup>&frasl;<sub>{{ denominator }}</sub>
    </span>
    <div
      class="button"
      @click="increase"
    >
      +
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScaleInput',
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
  watch: {
    fraction () {
      this.$emit('input', this.fraction)
    }
  },
  methods: {
    increase () {
      if (!isNaN(Number(this.numerator)) || !isNaN(Number(this.denominator))) {
        if (this.denominatorHidden) {
          this.numerator = Number(this.numerator) + 1
        } else if (this.denominator > 2) {
          this.denominator = this.denominator - 1
        } else {
          this.denominator = 1
          this.denominatorHidden = true
        }
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
}
</script>

<style lang="scss" scoped>
@import '@/modules/variables.scss';

.scale {
  display: inline-block;
  box-sizing: border-box;
  border: solid 1px #ccc;
}

.button {
  user-select: none;
  display: inline-block;
  text-align: center;
  width: 25px;

  @media screen and (max-width: 500px) {
    width: 35px;
  }

  &:hover {
    background-color: $font_color;
    color: white;
    cursor: pointer;
  }
}

span {
  display: inline-block;
  padding: 0 2px 0 2px;
  width: 18px;

  @media screen and (max-width: 500px) {
    width: 23px;
  }

  &.fraction {
    font-size: 10px;
    line-height: 15px;
    @media screen and (max-width: 500px) {
      line-height: 22px;
      font-size: 14px;
    }
  }
}
</style>
