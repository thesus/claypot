<template>
  <div class="scale">
    <button
      class="button"
      @click="quickDecrease"
    >-</button>

    <span class="button number" @click="showModal = true">
      <span class="full" v-if="full > 0">{{ full }}</span>
      <span class="fraction" v-if="remainder !== 0">
        <sup>{{ remainder }}</sup>
        /
        <sub>{{ denominator }}</sub>
      </span>
    </span>

    <button
      class="button"
      @click="quickIncrease"
    >+</button>

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

        <span class="helptext meals">{{ $t('recipe_detail.portion_count') }}</span>

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

        <span class="helptext size">{{ $t('recipe_detail.portion_size') }}</span>
        <span class="equals">=</span>
        <span class="result">{{ resultStr }}</span>
      </div>
    </Modal>
  </div>
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
      return new Intl.NumberFormat("en", { maximumFractionDigits: 2 }).format(this.result)
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
@import '@/modules/variables.scss';

.scale {
  display: inline-block;
  box-sizing: border-box;
  border: solid 1px #ccc;

	display: inline-flex;
	flex-direction: row;
  vertical-align: top;
	height: 26px;
  margin: 2px 5px 2px 2px;


  @media screen and (max-width: 500px) {
		height: 42px;
	}
}

.button {
  user-select: none;
  display: block;
  text-align: center;
  min-width: 25px;
	border: none;
	height: 100%;
  background-color: transparent;
  margin: 0;

  @media screen and (max-width: 500px) {
    min-width: 35px;
  }

  &:hover {
    background-color: $font_color;
    color: white;
    cursor: pointer;
  }

	&.number {
		height: 100%;
		cursor: pointer;
		padding-left: 8px;
		padding-right: 8px;

		.fraction {
			font-size: 13px;
			line-height: 16px;
		}

		.full {
			margin-right: 2px;
		}
	}
}

.box {
  display: grid;
  grid-template-columns: 30px 80px 30px 60px 150px 80px 100px;
  grid-template-rows: 30% 30% 30% 10%;
  grid-template-areas:
    ". . . . fraction . ."
    "decrease number increase times fraction equals result"
    ". . . . fraction . ."
    ". meals . . size . .";
  place-items: center;
  font-size: 300%;

  .input {
    border: 0px;
    background-color: transparent;
    text-align: center;
    height: 100%;
    font-size: 100%;
  }

  /* Informational text in modal */
  .helptext {
    font-size: 50%;
  }

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
  }

  .times {
    grid-area: times;
  }

  /* Fraction split in 2 grid layouts */
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
      grid-template-columns: 25% 50% 25%;
      grid-template-areas: "decrease number increase";
      place-items: center;

      /* Fraction line, thicker on desktops */
      &.nominator {
        border-bottom: solid 3px $font_color;
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
  }

  @media screen and (max-width: 630px) {
    /* Smaller layout on mobile devices */
    grid-template-columns: 35px 30px 35px 20px 100px 20px 20px;
    font-size: 100%;

    .btn {
      width: 35px;
      height: 35px;
    }

    .helptext {
      font-size: 90%;
    }

    .fraction {
      .block {
        grid-template-columns: 35% 30% 35%;

        &.nominator {
          border-width: 1px;
        }
      }
    }
  }
}
</style>
