<template>
  <div v-if="errors">
    <p v-if="errors.length === 1">{{ errors[0] }}</p>
    <ul v-else>
      <li v-for="(err, i) in errors" :v-key="i">
        <p>{{ err }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'form-field-validation-error',
  props: {
    errors: Array
  }
}
</script>
