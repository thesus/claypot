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
      <div class="fraction-modal">
        <div class="number-box has-btns">
          <div>
            <button
              class="btn"
              @click="increaseMultiplyer"
            >+</button>
          </div>
          <div>
            <input
              class="input full"
              min="1"
              :value="multiplyer"
            >
            <span style="position: relative; bottom: 1.5em;">{{ $t('recipe_detail.portion_count') }}</span>
          </div>
          <div>
            <button
              class="btn"
              @click="decreaseMultiplyer"
            >-</button>
          </div>
        </div>
        <div class="calc-hint">×</div>
        <div class="fraction has-btns">
          <div class="number-box">
            <div>
              <button
                class="btn"
                @click="decreaseNumerator"
              >-</button>
            </div>
            <div>
              <input
                class="input"
                min="1"
                :value="numerator"
              >
            </div>
            <div>
              <button
                class="btn"
                @click="increaseNumerator"
              >+</button>
            </div>
          </div>
          <div class="number-box">
            <div>
              <button
                class="btn"
                @click="decreaseDenominator"
              >-</button>
            </div>
            <div>
              <input
                class="input denominator"
                min="1"
                :value="denominator"
              >
            </div>
            <div>
              <button
                class="btn"
                @click="increaseDenominator"
              >+</button>
            </div>
          </div>
          <span style="position: relative; bottom: 0.0em;">{{ $t('recipe_detail.portion_size') }}</span>
        </div>
        <div class="calc-hint">={{ resultStr }}</div>
      </div>
    </Modal>
  </span>
</template>

<script>
import Modal from '@/components/utils/Modal'

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

input {
  /*border: 0px;*/
  text-align: center;
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

.fraction-modal {
  width: 50vw;
  display: flex;
  flex-direction: row;

  .has-btns div:nth-child(odd) {
    /* vertical align of buttons */
    margin: auto;
  }

  & > .number-box {
    display: flex;
    flex-direction: row;
  }

  .calc-hint {
    font-size: 400%;
    margin: auto;
    white-space: nowrap;
  }

  .full {
    height: 100%;
    font-size: 600%;
    border: 0px;
  }

  .fraction {
    margin: auto;
    display: flex;
    flex-direction: column;
    position: relative;

    & > .number-box {
      display: flex;
      flex-direction: row;

      & > div {
        flex: 1;
      }
    }

    input {
      height: 100%;
      font-size: 300%;
      border-width: 0px;
    }
    & > div:first-child {
      border-bottom: 4px solid black;
    }
  }
}
</style>
