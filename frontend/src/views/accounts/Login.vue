<template>
  <div>
    <div class="login">
      <form @submit.prevent="submit">
        <input
          ref="username_input"
          v-model="credentials.username"
          :placeholder="$t('login.username')"
          :class="{'form-error': !!errors.username.length}"
          autofocus
          type="text"
        >
        <FormFieldValidationError :errors="errors.username" />
        <input
          v-model="credentials.password"
          :placeholder="$t('login.password')"
          :class="{'form-error': !!errors.password.length}"
          type="password"
        >
        <FormFieldValidationError :errors="errors.password" />

        <FormFieldValidationError :errors="errors.other" />
        <router-link
          :to="{ name: 'reset-password' }"
          tabindex="-1"
        >
          {{ $t('login.forgot_password') }}
        </router-link>
        <router-link
          :to="{ name: 'signup' }"
          tabindex="-1"
        >
          {{ $t('login.signup') }}
        </router-link>
        <button
          type="submit"
          class="btn right"
        >
          {{ $t('login.login') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'

export default {
  components: {
    FormFieldValidationError
  },
  data: () => {
    return {
      credentials: {
        username: null,
        password: null,
      },
      errors: {
        username: [],
        password: [],
        other: [],
      },
    }
  },
  mounted () {
    this.$refs.username_input.focus()
  },
  methods: {
    async submit () {
      try {
        await this.$store.dispatch('login', this.$data.credentials)
      } catch(err) {
        if (err instanceof InvalidRequestError) {
          this.errors.username = err.response.username || []
          this.errors.password = err.response.password || []
          this.errors.other = err.response.non_field_errors || []
        } else {
          this.errors.other = [err.message]
        }
      }
    }
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/small_form.scss';

a {
  float: left;
  font-size: 14px;
  margin: 2px 8px 0 1px;
}
</style>
