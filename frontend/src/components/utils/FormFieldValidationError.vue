<template>
  <div v-if="errors">
    <p v-if="errors.length === 1">
      {{ errors[0] }}
    </p>
    <ul v-else>
      <li
        v-for="(err, i) in errors"
        :key="i"
      >
        <p>{{ err }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'FormFieldValidationError',
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
  }
}
</script>

<style lang="scss" scoped>
  p, ul {
    margin: 0;
  }
</style>
