<template>
  <div class="scale">
    <Modal
      v-if="modal"
      :title="$t('scaling.title')"
      @close="modal = false"
      class="modal"
    >

      <sup>
        <button
          class="btn"
          @click="increaseNumerator"
          :disabled="denominator < 2"
        >
          +
        </button>
      </sup>
      &frasl;
      <sub>
        <button
          class="btn"
          @click="changeDenominator(+1)"
        >
          +
        </button>
      </sub>
      <button
        class="btn full"
        @click="increaseFull"
      >
        +
      </button>


      <div class="extended">
        <span
          v-if="!isInteger"
          class="fraction"
          :class="{ 'ignore': displayNumerator === 0 }"
        >
          <sup>{{ displayNumerator }}</sup>
          &frasl;
          <sub>{{ denominator }}</sub>
        </span>
        <span
          v-if="n > 0"
          class="full"
        >
          {{ n }}
        </span>
      </div>

      <sup>
        <button
          class="btn"
          :disabled="denominator < 2 || (n === 0 && numerator < 2)"
          @click="decreaseNumerator"
        >
          -
        </button>
      </sup>
      &frasl;
      <sub>
        <button
          class="btn"
          :disabled="denominator < 2"
          @click="changeDenominator(-1)"
        >
          -
        </button>
      </sub>
      <button
        class="btn full"
        :disabled="n === 0"
        @click="decreaseFull"
      >
        -
      </button>
    </Modal>


    <div class="button" @click="decreaseSimple">-</div>
    <div class="extended" @click="modal = true">
      <span
        v-if="!isInteger"
        class="fraction"
        :class="{ 'ignore': displayNumerator === 0 }"
      >
        <sup>{{ displayNumerator }}</sup>
        &frasl;
        <sub>{{ denominator }}</sub>
      </span>
      <span
        v-if="n > 0"
        class="full"
      >
        {{ n }}
      </span>
    </div>
    <div
      class="button"
      @click="increaseSimple"
    >
      +
    </div>
  </div>
</template>

<script>
import Modal from '@/components/Modal'


export default {
  name: 'ScaleInput',
  components: {
    Modal
  },
  data () {
    return {
      denominator: 1,
      numerator: 1,
      denominatorHidden: true,
      modal: false
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
    displayNumerator () {
      if (this.numerator / this.denominator >= 1) {
        return this.numerator % this.denominator
      } else {
        return this.numerator
      }
    },
    n () {
      return Math.floor(this.numerator / this.denominator)
    },
    isInteger () {
      return this.denominator === 1
    }
  },
  watch: {
    fraction () {
      this.$emit('input', this.fraction)
    }
  },
  methods: {
    increaseNumerator () {
      this.numerator++
    },
    decreaseNumerator () {
      if (this.numerator >= 1) {
        this.numerator--
      }
    },
    changeDenominator (v) {
      if (this.denominator + v >= 1) {
        let c = Math.floor(this.numerator / this.denominator)
        let n = this.numerator % this.denominator

        this.denominator += v
        this.numerator = this.denominator * c + n
      }
    },
    increaseFull () {
      this.numerator += this.denominator
    },
    decreaseFull () {
      this.numerator -= this.denominator
    },
    increaseSimple () {
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
    decreaseSimple () {
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
@import '@/modules/inputs.scss';
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


.simple {
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

.extended {
  .full {
    margin-left: 4px;
  }

  .fraction {
    &.ignore {
      color: gray;
    }
  }
}

.modal {
  .btn {
    height: initial;

    &.full {
      margin-left: 4px;
    }
  }
}
</style>
