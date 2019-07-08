<template>
  <div class="synonyms">
    <div v-if="dirty.length > 0">
      <span>{{ $t('synonym.synonym') }}</span>
      <div
        v-for="(item, index) in dirty"
        :key="index"
        class="input"
      >
        <div class="wrapper">
          <IngredientInput
            :value="item"
            :error="!!synonymError(index).length"
            @input="$set(dirty, index, $event)"
          />
          <FormFieldValidationError :errors="synonymError(index)" />
        </div>
        <button
          class="btn"
          @click="dirty.splice(index, 1)"
        >
          {{ $t('generic.remove') }}
        </button>
      </div>
    </div>
    <span v-else>{{ $t('synonym.no_synonym') }}</span>
    <button
      class="btn right"
      @click="dirty.push('')"
    >
      {{ $t('synonym.add') }}
    </button>
    <div style="clear: both;" />
  </div>
</template>

<script>
import IngredientInput from '@/components/IngredientInput'
import FormFieldValidationError from '@/components/FormFieldValidationError'

export default {
  components: {
    IngredientInput,
    FormFieldValidationError
  },
  props: {
    value: {
      type: Array,
      default: () => []
    },
    errors: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      dirty: [...this.value]
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
      this.dirty.splice(0, this.dirty.length, ...this.value)
    },
    dirty () {
      if (!this.isEqual) {
        this.$emit('input', [...this.dirty])
      }
    }
  },
  methods: {
    synonymError (i) {
      return this.errors[i] || []
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.input {
  display: flex;
  margin: 2px 0 2px 0;

  .btn {
    height: 30px;
    margin: 0 0 0 3px;
    @media screen and (max-width: 500px) {
      height: 40px;
    }
  }
}

.synonyms {
  padding: 5px;
  background: rgba(184, 203, 214, 0.4);

  .wrapper {
    width: 100%;
  }
}
</style>
