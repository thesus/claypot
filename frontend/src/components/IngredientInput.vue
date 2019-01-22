<template>
  <div>
    <div class="suggestions" v-if="showSuggestions && suggestions.length">
      <ul>
        <li v-for="(suggestion, i) in suggestions" :key="i" :class="{highlighted: isHighlighted(i)}" @click="applySuggestion(i)">{{ suggestion }}</li>
      </ul>
    </div>
    <input
      v-model="dirtyValue"
      @focus="onFocus"
      @blur="onBlur"
      @keyup.down="moveHighlightDown()"
      @keyup.up="moveHighlightUp()"
      @keyup.enter="applySuggestion()"
      @input="updateSuggestions"
    />
  </div>
</template>

<script>
import {api, endpoints} from '@/api'

export default {
  name: 'ingredient-input',
  props: {
    value: String,
  },
  data () {
    return {
      dirtyValue: '',
      suggestions: [],
      showSuggestions: false,
      highlighted: false,
    }
  },
  mounted () {
    this.dirtyValue = this.value
  },
  watch: {
    value (v) {
      this.dirtyValue = v
    },
    dirtyValue (v) {
      this.$emit('input', v)
    },
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
    onBlur () {
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

.suggestions {
  border: 1px solid pink;
  background-color: white;
  position: absolute;
  top: 100%;
  display: inline;
  z-index: 1;
  width: 12em;
  ul {
    list-style-type: none;
    padding-left: 0;
  }
}


.highlighted {
  background-color: lime;
}
</style>
