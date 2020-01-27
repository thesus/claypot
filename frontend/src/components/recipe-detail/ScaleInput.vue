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
      @click="doShowModal"
    >
      <template v-if="mode === MODE_CLOSED || mode === MODE_ADVANCED">
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
      </template>
      <template v-else>
        <span>
          {{ round(scaleToAmount) }}&nbsp;{{ scaleToIngredient.unit }} {{ scaleToIngredient.ingredient }}
          <!-- show ingredient unit and name - unfortunately lost right now -->
        </span>
      </template>
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
      <!-- MODE_SCALE_TO -->
      <form
        v-if="mode == MODE_SCALE_TO"
        class="scaleTo"
        @submit="scaleTo"
      >
        <select
          v-model="scaleToIngredient"
          @change="reverseScaleTo"
        >
          <optgroup
            v-for="group in scaleToOptions"
            :key="group.key"
            :label="group.text"
          >
            <option
              v-for="item in group.items"
              :key="item.key"
              :value="item"
            >
              {{ item.text }}
            </option>
          </optgroup>
        </select>
        <span>{{ $t("recipe_detail.scale_to.middle_text") }}</span>
        <input
          v-model="dirtyAmount"
          type="number"
          step="any"
        >
        <button
          class="btn"
          role="submit"
        >
          {{ $t('recipe_detail.scale_to.submit') }}
        </button>
      </form>
      <!-- MODE_ADVANCED -->
      <div
        v-if="mode == MODE_ADVANCED"
        class="box"
      >
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

      <!-- list a quick summary of all ingredients, scaled by the current multiplier -->
      <ol class="ingredientList">
        <li
          v-for="(item, i) in scaledIngredients"
          :key="i"
        >
          {{ item.amount }}{{ item.unit }}&nbsp;{{ item.ingredient }}<template v-if="i < scaledIngredients.length - 1">,</template>
        </li>
      </ol>

      <!-- toggle between MODE_SCALE_TO and MODE_ADVANCED -->
      <div class="modeswitch">
        <label>
          <input
            type="checkbox"
            :checked="mode === MODE_ADVANCED"
            @change="toggleMode"
          >
          {{ $t("recipe_detail.scale_to.advanced_mode") }}
        </label>
      </div>
    </Modal>
  </div>
</template>

<script>
import Modal from '@/components/utils/Modal'

const MODE_CLOSED = "closed"
const MODE_SCALE_TO = "scale_to"
const MODE_ADVANCED = "advanced"

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
      mode: MODE_CLOSED,
      scaleToAmount: null,
      dirtyAmount: "0",
      scaleToIngredient: { value: null } ,
      formatter: new Intl.NumberFormat(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 2, useGrouping: false}),
    }
  },
  computed: {
    AMOUNT_TYPE_NUMERIC () {
      return 2
    },
    MODE_ADVANCED: () => MODE_ADVANCED,
    MODE_CLOSED: () => MODE_CLOSED,
    MODE_SCALE_TO: () => MODE_SCALE_TO,
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
          text: group.title != "" ? group.title : this.$t('recipe_detail.scale_to.ingredient_group'),
          key: String(c1),
          items: group.ingredients
            .filter(i => (i.amount_type == this.AMOUNT_TYPE_NUMERIC && i.unit !== ''))
            .map((i, c2) => ({
              text: i.ingredient + " (" + String(i.amount_numeric) + String(i.unit) + ")",
              ingredient: i.ingredient,
              unit: i.unit,
              value: i.amount_numeric,
              key: String(c1) + "-" + String(c2),
            }))
        }))
        .filter(group => group.items.length > 0)
    },
    scaledIngredients () {
      return [].concat(
        ...this.scaleToOptions
        .map(group => group.items.map(i => ({
          ingredient: i.ingredient,
          unit: i.unit,
          amount: this.formatter.format(this.multiplier * this.numerator / this.denominator * i.value),
        })))
      )
    },
  },
  watch: {
    scaleToAmount () {
      // Set the dirty amount to current scaled mode. We can do that, since changing
      // `this.dirtyAmount` does not trigger any action by itself
      this.dirtyAmount = String(this.round(this.scaleToAmount))
    },
    result () {
      this.$emit('input', this.result)
    },
  },
  methods: {
    round(value) {
      // Number.EPSILON is because floating point division in javascript
      return Math.round((Number.EPSILON + value) * 100) / 100
    },
    doShowModal () {
      // Show actual modal dialog
      this.showModal = true

      // If the modal has never been loaded, we will switch to MODE_SCALE_TO
      if (this.mode === MODE_CLOSED) {
        this.mode = MODE_SCALE_TO
      }

      /*
       Preselect ingredient with highest numeric amount.
       This is trying to be helpful by doing what we expect most users
       to want most of the time.
      */
      {
        let maxIngredient = { value: null }
        this.scaleToOptions.forEach(i => {
          i.items.forEach(j => {
            if (maxIngredient.value === null || j.value > maxIngredient.value) {
              maxIngredient = j
            }
          })
        })
        if (maxIngredient !== null) {
          this.scaleToIngredient = maxIngredient
          this.reverseScaleTo()
        }
      }
    },
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
      if (this.mode === MODE_CLOSED || this.mode === MODE_ADVANCED)
      {
        if (this.multiplier === 1) {
          if (this.denominator <= 1) {
            this.numerator += 1
          } else {
            this.denominator -= 1
          }
        } else {
          this.multiplier += 1
        }
      } else {
        this.multiplier += 1
      }
      this.reverseScaleTo()
    },
    quickDecrease () {
      if (this.mode === MODE_CLOSED || this.mode === MODE_ADVANCED)
      {
        if (this.multiplier === 1) {
          if (this.numerator > 1) {
            this.numerator -= 1
          } else {
            this.denominator += 1
          }
        } else {
          this.multiplier = Math.max(this.multiplier - 1, 1)
        }
      } else {
        // MODE_SCALE_TO
        if (this.multiplier > 1) {
          this.multiplier -= 1
        }
      }
      this.reverseScaleTo()
    },
    scaleTo () {
      this.multiplier = 1
      this.numerator = Number(this.dirtyAmount)
      this.denominator = Number(this.scaleToIngredient.value)

      // For displaying purposes
      this.reverseScaleTo()
    },
    reverseScaleTo () {
      this.scaleToAmount = this.multiplier * this.numerator / this.denominator * this.scaleToIngredient.value
    },
    toggleMode () {
      this.mode = this.mode === MODE_SCALE_TO ? MODE_ADVANCED : MODE_SCALE_TO
      this.multiplier = 1
      this.numerator = 1
      this.denominator = 1
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

  &:hover {
    background-color: $font_color;
    color: white;
    cursor: pointer;
  }

	&.number {
    line-height: 24px;
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

  @media screen and (max-width: 500px) {
    min-width: 35px;

    &.number {
      line-height: 40px;
    }
  }
}

.box {
  display: grid;
  grid-template-columns: 6% 15% 6% 12% 30% 15% 16%;
  grid-template-rows: 30% 30% 30% 10%;
  grid-template-areas:
    ". . . . fraction . ."
    "decrease number increase times fraction equals result"
    ". . . . fraction . ."
    ". meals . . size . .";
  place-items: center;
  font-size: 300%;
  width: 100%;

  .input {
    border: 0px;
    background-color: transparent;
    text-align: center;
    height: 100%;
    font-size: 100%;
  }

  /* Remove step buttons on inputs */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
   -webkit-appearance: none;
    margin: 0;
  }

  /* Don't indent numbers in 'hidden' inputs */
  input[type=number] {
    -moz-appearance: textfield;
    text-indent: 0px;
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
    grid-template-columns: 13% 11% 13% 7% 42% 7% 7%;
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
        grid-template-columns: 33% 33% 33%;

        &.nominator {
          border-width: 1px;
        }
      }
    }
  }
}

.scaleTo {
  display: flex;
  flex-direction: row;
  justify-content: space-between;

  .btn {
    min-width: unset;
    /* same height as inputs */
    height: 30px;
  }

  input, select, span {
    margin: 2px;
  }

  input, select {
    min-width: 20%;
    width: auto;
  }

  span {
    min-width: 70px;
    line-height: 30px;
  }

  @media screen and (max-width: 500px) {
    flex-direction: column;
  }
}

ol.ingredientList {
  & li {
    display: inline;
  }
}
</style>
