<template>
  <div>
    <div class="signup">
      <form @submit.prevent="submit">
        <h5>{{ $t('signup.heading') }}</h5>
        <input
          v-model="form.email"
          :placeholder="$t('signup.email')"
          :class="{'form-error': !!getErrors.email.length}"
          type="email"
          :disabled="disabled"
        >
        <FormFieldValidationError :errors="getErrors.email" />
        <input
          v-model="form.username"
          :placeholder="$t('signup.username')"
          :class="{'form-error': !!getErrors.username.length}"
          type="text"
          :disabled="disabled"
        >
        <FormFieldValidationError :errors="getErrors.username" />
        <input
          v-model="form.password1"
          :placeholder="$t('signup.password')"
          :class="{'form-error': !!getErrors.password1.length}"
          type="password"
          :disabled="disabled"
        >
        <FormFieldValidationError :errors="getErrors.password1" />
        <input
          v-model="form.password2"
          :placeholder="$t('signup.password_again')"
          :class="{'form-error': !!getErrors.password2.length}"
          type="password"
          :disabled="disabled"
        >
        <FormFieldValidationError :errors="getErrors.password2" />

        <FormFieldValidationError :errors="getErrors.other" />

        <p v-if="finished">
          {{ $t("signup.confirm") }}
        </p>
        <button
          type="submit"
          class="btn right"
          :disabled="disabled"
        >
          {{ $t('signup.signup') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { api, endpoints,InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'

export default {
  components: {
    FormFieldValidationError,
  },
  data: () => {
    return {
      form: {
        username: null,
        email: null,
        password1: null,
        password2: null
      },
      errors: {},

      finished: false,
      working: false
    }
  },
  computed: {
    getErrors() {
      return {
        username: [],
        email: [],
        password1: [],
        password2: [],
        other: [],

        ...this.errors,
      }
    },
    disabled() {
      return this.finished || this.working
    }
  },
  methods: {
    async submit () {
      this.working = true

      try {
        const response = await api(
          endpoints.signup(),
          this.$data.form,
        )

        if (!response.ok) {
          throw new InvalidRequestError(
            response.status,
            await response.json(),
          )
        }

        this.errors = {}
        this.finished = true;
      } catch (err) {
        if (err instanceof InvalidRequestError) {
          this.errors = {
            ...err.response
          }
        } else {
          this.$set(this.errors, 'other', [this.$t("signup.unknown_error") ])
        }
      } finally {
        this.working = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/small_form.scss';
</style>
