<template>
  <div class="scale">
    <button
      class="button"
      @click="quickDecrease"
    >
      -
    </button>

    <span
      class="button number"
      @click="showModal = true"
    >
      <span
        v-if="full > 0"
        class="full"
      >{{ full }}</span>
      <span
        v-if="remainder !== 0"
        class="fraction"
      >
        <sup>{{ remainder }}</sup>
        /
        <sub>{{ denominator }}</sub>
      </span>
    </span>

    <button
      class="button"
      @click="quickIncrease"
    >
      +
    </button>

    <Modal
      v-if="showModal"
      @close="showModal = false"
    >
      <form
        class="scaleTo"
        @submit="scaleTo"
      >
        <select v-model="scaleToIngredient">
          <optgroup
            v-for="group in scaleToOptions"
            :key="group.key"
            :label="group.text"
          >
            <option
              v-for="item in group.items"
              :key="item.key"
              :value="item.value"
            >
              {{ item.text }}
            </option>
          </optgroup>
        </select>
        <div>{{ $t("recipe_detail.scale_to.middle_text") }}</div>
        <input v-model="scaleToAmount">
        <button
          class="btn"
          role="submit"
        >
          {{ $t('recipe_detail.scale_to.submit') }}
        </button>
      </form>

      <div class="box">
        <button
          class="btn increase"
          @click="increaseMultiplier"
        >
          +
        </button>

        <input
          v-model.number="multiplier"
          class="input number"
          min="1"
          type="number"
        >

        <span class="helptext meals">{{ $t('recipe_detail.portion_count') }}</span>

        <button
          class="btn decrease"
          :disabled="!canDecreaseMultiplier"
          @click="decreaseMultiplier"
        >
          -
        </button>

        <div class="times">
          ×
        </div>
        <div class="fraction">
          <div class="block nominator">
            <button
              class="btn decrease"
              :disabled="!canDecreaseNumerator"
              @click="decreaseNumerator"
            >
              -
            </button>
            <input
              v-model.number="numerator"
              class="input number"
              min="1"
              type="number"
            >
            <button
              class="btn increase"
              @click="increaseNumerator"
            >
              +
            </button>
          </div>
          <div class="block">
            <button
              class="btn decrease"
              :disabled="!canDecreaseDenominator"
              @click="decreaseDenominator"
            >
              -
            </button>
            <input
              v-model.number="denominator"
              class="input number"
              min="1"
              type="number"
            >
            <button
              class="btn incrDenominator"
              @click="increaseDenominator"
            >
              +
            </button>
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
    recipe: {
      type: Object,
      default: () => ({}),
    },
  },
  data () {
    return {
      multiplier: 1.0,
      numerator: 1.0,
      denominator: 1.0,
      showModal: false,
      scaleToAmount: null,
      scaleToIngredient: null,
    }
  },
  computed: {
    AMOUNT_TYPE_NUMERIC () {
      return 2
    },
    full () {
      return Math.floor(this.multiplier * this.numerator / this.denominator)
    },
    result () {
      return this.multiplier * (this.numerator / this.denominator)
    },
    resultStr () {
      return new Intl.NumberFormat("en", { maximumFractionDigits: 2 }).format(this.result)
    },
    remainder () {
      return (this.multiplier * this.numerator) % this.denominator
    },
    canDecreaseDenominator () {
      return this.denominator >= 2
    },
    canDecreaseNumerator () {
      return this.numerator >= 2
    },
    canDecreaseMultiplier () {
      return this.multiplier >= 2
    },
    scaleToOptions () {
      return this.recipe.ingredients
        .map((group, c1) => ({
          text: group.is_group ? group.title : this.$t('recipe_detail.scale_to.ingredient_group'),
          key: String(c1),
          items: group.ingredients
            .filter(i => (i.amount_type == this.AMOUNT_TYPE_NUMERIC && i.unit !== ''))
            .map((i, c2) => ({
              text: i.ingredient + " (" + String(i.amount_numeric) + String(i.unit) + ")",
              value: i.amount_numeric,
              key: String(c1) + "-" + String(c2),
            }))
        }))
        .filter(group => group.items.length > 0)
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
      this.reverseScaleTo()
    },
    decreaseNumerator () {
      this.numerator = Math.max(this.numerator - 1, 1)
      this.reverseScaleTo()
    },
    increaseDenominator () {
      this.denominator += 1
      this.reverseScaleTo()
    },
    decreaseDenominator () {
      this.denominator = Math.max(this.denominator - 1, 1)
      this.reverseScaleTo()
    },
    increaseMultiplier () {
      this.multiplier += 1
      this.reverseScaleTo()
    },
    decreaseMultiplier () {
      this.multiplier = Math.max(this.multiplier - 1, 1)
      this.reverseScaleTo()
    },
    quickIncrease () {
      if (this.multiplier === 1) {
        if (this.denominator <= 1) {
          this.numerator += 1
        } else {
          this.denominator -= 1
        }
      } else {
        this.multiplier += 1
      }
      this.reverseScaleTo()
    },
    quickDecrease () {
      if (this.multiplier === 1) {
        if (this.numerator > 1) {
          this.numerator -= 1
        } else {
          this.denominator += 1
        }
      } else {
        this.multiplier = Math.max(this.multiplier - 1, 1)
      }
      this.reverseScaleTo()
    },
    scaleTo () {
      // TODO: reduce fraction
      this.multiplier = 1
      this.numerator = Number(this.scaleToAmount)
      this.denominator = Number(this.scaleToIngredient)
    },
    reverseScaleTo () {
      this.scaleToAmount = this.multiplier * this.numerator / this.denominator * this.scaleToIngredient
    }
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

/* Remove step buttons on inputs */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
 -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance:textfield;
}

.scaleTo {
  display: flex;
  flex-direction: column;
}
</style>
