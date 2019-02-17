<template>
  <div class="wrapper">
    <div
      v-if="showSuggestions && suggestions.length"
      class="suggestions">
      <ul>
        <li
          v-for="(suggestion, i) in suggestions"
          :key="i"
          :class="{highlighted: isHighlighted(i)}"
          @mouseover="highlightThis(i)"
          @mouseout="highlighted = false"
          @mousedown="applySuggestion(i)"
        >{{ suggestion }}</li>
      </ul>
    </div>
    <input
      v-model="dirtyValue"
      bubbles="true"
      @focus="onFocus()"
      @blur="onBlur()"
      @keyup.down="moveHighlightDown()"
      @keyup.up="moveHighlightUp()"
      @keyup.enter="applySuggestion()"
      @input="updateSuggestions"
    >
  </div>
</template>

<script>
import {api, endpoints} from '@/api'

export default {
  name: 'IngredientInput',
  props: {
    value: {
      type: String,
      default: '',
    },
  },
  data () {
    return {
      dirtyValue: '',
      suggestions: [],
      showSuggestions: false,
      highlighted: false,
    }
  },
  watch: {
    value (v) {
      this.dirtyValue = v
    },
    dirtyValue (v) {
      this.$emit('input', v)
    },
  },
  mounted () {
    this.dirtyValue = this.value
  },
  methods: {
    async updateSuggestions () {
      this.suggestions.length = 0
      if (this.dirtyValue.length === 0) {
        this.closeSuggestions()
        return
      }
      try {
        const r = await api(endpoints.search_ingredients(this.dirtyValue))
        if (r.ok) {
          const d = await r.json()
          for (let ingredient of d) {
            this.suggestions.push(ingredient.name)
          }
        } else {
          // TODO: Present propert error message
          throw new Error('')
        }
      } catch (err) {
        // TODO: Present error to user
      }
      if (this.suggestions.length > 0) {
        this.openSuggestions()
      }
    },
    isHighlighted (i) {
      return this.highlighted !== false && this.highlighted === i
    },
    onFocus () {
      this.updateSuggestions()
    },
    async onBlur () {
      this.closeSuggestions()
    },
    openSuggestions () {
      this.showSuggestions = true
      this.highlighted = false
    },
    closeSuggestions () {
      this.showSuggestions = false
      this.highlighted = false
    },
    moveHighlightDown () {
      if (this.highlighted !== false) {
        this.highlighted++
      } else {
        this.highlighted = 0
      }
      if (this.highlighted >= this.suggestions.length) {
        this.highlighted = false
      }
    },
    moveHighlightUp () {
      if (this.highlighted !== false) {
        this.highlighted--
      } else {
        this.highlighted = this.suggestions.length - 1
      }
      if (this.highlighted < 0) {
        this.highlighted = false
      }
    },
    highlightThis (i) {
      this.highlighted = i;
    },
    applySuggestion (highlighted) {
      if (typeof highlighted !== "undefined") {
        this.highlighted = highlighted
      }
      if (this.highlighted !== false) {
        this.dirtyValue = this.suggestions[this.highlighted]
      }
      this.closeSuggestions()
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
.wrapper {
  width: 100%;
  position: relative;
  overflow: visible;
  outline: none;
}

.suggestions {
  border: 1px solid #ccc;
  background-color: white;
  position: absolute;
  top: 26px;
  z-index: 100;
  width: 100%;
  min-height: 22px;
  box-sizing: border-box;

  ul {
    list-style-type: none;
    padding-left: 0;
    margin: 0;
    li {
      cursor: pointer;
    }
  }
}

.highlighted {
  background-color: rgba(52, 73, 94, 0.1);
}
</style>
