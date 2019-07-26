<template>
  <span>
    <span class="pointer">
      <button
        class="btn"
        @click="quickDecrease"
      >-</button>
      <span class="number" @click="showModal = true">
        <span v-if="full > 0">{{ full }}</span>
        <span v-if="remainder !== 0">
          <sup>{{ remainder }}</sup>
          /
          <sub>{{ denominator }}</sub>
        </span>
      </span>
      <button
        class="btn"
        @click="quickIncrease"
      >+</button>
    </span>
    <Modal
      v-if="showModal"
      @close="showModal = false"
    >
      <div class="box">
        <button
          class="btn increase"
          @click="increaseMultiplyer"
        >+</button>

        <input
          class="input number"
          min="1"
          :value="multiplyer"
        >

        <span class="meals">{{ $t('recipe_detail.portion_count') }}</span>

        <button
          class="btn decrease"
          @click="decreaseMultiplyer"
        >-</button>

        <div class="times">×</div>
        <div class="fraction">
          <div class="block nominator">
            <button
              class="btn decrease"
              @click="decreaseNumerator"
            >-</button>
            <input
              class="input number"
              min="1"
              :value="numerator"
            >
            <button
              class="btn increase"
              @click="increaseNumerator"
            >+</button>
          </div>
          <div class="block">
            <button
              class="btn decrease"
              @click="decreaseDenominator"
            >-</button>
            <input
              class="input number"
              min="1"
              :value="denominator"
            >
            <button
              class="btn incrDenominator"
              @click="increaseDenominator"
            >+</button>
          </div>
        </div>

        <span class="size">{{ $t('recipe_detail.portion_size') }}</span>
        <span class="equals">=</span>
        <span class="result">{{ resultStr }}</span>
      </div>
    </Modal>
  </span>
</template>

<script>
import Modal from '@/components/Modal'

export default {
  components: {
    Modal,
  },
  props: {
    value: {
      type: Number,
      default: 1.0,
    },
  },
  data () {
    return {
      multiplyer: 1.0,
      numerator: 1.0,
      denominator: 1.0,
      showModal: false,
    }
  },
  computed: {
    full () {
      return Math.floor(this.multiplyer * this.numerator / this.denominator)
    },
    result () {
      return this.multiplyer * (this.numerator / this.denominator)
    },
    resultStr () {
      return new Intl.NumberFormat().format(this.result)
    },
    remainder () {
      return (this.multiplyer * this.numerator) % this.denominator
    },
  },
  watch: {
    result () {
      this.$emit('input', this.result)
    },
  },
  methods: {
    increaseNumerator () {
      this.numerator += 1
    },
    decreaseNumerator () {
      this.numerator = Math.max(this.numerator - 1, 1)
    },
    increaseDenominator () {
      this.denominator += 1
    },
    decreaseDenominator () {
      this.denominator = Math.max(this.denominator - 1, 1)
    },
    increaseMultiplyer () {
      this.multiplyer += 1
    },
    decreaseMultiplyer () {
      this.multiplyer = Math.max(this.multiplyer - 1, 1)
    },
    quickIncrease () {
      if (this.multiplyer === 1) {
        if (this.denominator <= 1) {
          this.numerator += 1
        } else {
          this.denominator -= 1
        }
      } else {
        this.multiplyer += 1
      }
    },
    quickDecrease () {
      if (this.multiplyer === 1) {
        if (this.numerator > 1) {
          this.numerator -= 1
        } else {
          this.denominator += 1
        }
      } else {
        this.multiplyer = Math.max(this.multiplyer - 1, 1)
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.input {
  border: 0px;
  text-align: center;
  font-size: 200%;
  height: 100%;
}

.pointer {
  cursor: pointer;
  padding-left: 8px;
  padding-right: 8px;

  .number {
    display: inline-block;
    min-width: 1.5em;
  }
}

.box {
  display: grid;
  grid-template-columns: 40px 80px 40px 80px 150px 80px 80px;
  grid-template-rows: 30% 30% 30% 10%;
  grid-template-areas:
    ". . . . fraction . ."
    "decrease number increase times fraction equals result"
    ". . . . fraction . ."
    ". meals . . size . .";
  place-items: center;
  font-size: 200%;

    .increase {
      grid-area: increase;
    }

    .decrease {
      grid-area: decrease;
    }

    .number {
      grid-area: number;
    }

    .meals {
      grid-area: meals;
      font-size: 60%;
    }

    .times {
      grid-area: times;
    }

    .fraction {
      grid-area: fraction;

      display: grid;
      grid-template-columns: 100%;
      grid-template-rows: 50% 50%;
      grid-template-areas:
        "numerator"
        "denominator";

      .block {
        display: grid;
        grid-template-columns: 20% 60% 20%;
        grid-template-areas: "decrease number increase";
        place-items: center;

        &.nominator {
          border-bottom: solid 1px black;
        }
      }
    }

    .equals {
      grid-area: equals;
    }

    .result {
      grid-area: result;
    }

    .size {
      grid-area: size;
      font-size: 60%;
    }
}
</style>
