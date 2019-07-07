<template>
  <div>
    <div
      v-for="(item, index) in dirty"
      :key="index"
      class="input"
    >
      <IngredientInput
        :value="item"
        @input="$set(dirty, index, $event)"
      />
      <button
        class="btn"
        @click="dirty.splice(index, 1)"
      >
        Remove
      </button>
    </div>
    <button
      class="btn"
      @click="dirty.push('')"
    >
      Add
    </button>
  </div>
</template>

<script>
import IngredientInput from '@/components/IngredientInput'

export default {
  components: {
    IngredientInput
  },
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      dirty: []
    }
  },
  computed: {
    isEqual () {
      return (
        this.value.length === this.dirty.length &&
        this.value.every((value, index) => value === this.dirty[index])
      )
    }
  },
  watch: {
    value () {
      this.$set(this, 'dirty', JSON.parse(JSON.stringify(this.value)))
    },
    dirty: {
      handler () {
        if (!this.isEqual) {
          this.$emit('input', this.dirty)
        }
      }
    }
  },
  mounted () {
    this.$set(this, 'dirty', JSON.parse(JSON.stringify(this.value)))
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.input {
  display: flex;
  margin: 2px 0 2px 0;
}
</style>
