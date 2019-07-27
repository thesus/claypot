<template>
  <div>
    <div class="reset-confirm">
      <form @submit.prevent="submit">
        <input
          v-model="form.new_password1"
          :placeholder="$t('reset_password_confirm.password')"
          blank="false"
          type="password"
        >
        <FormFieldValidationError :errors="errors.new_password1" />
        <input
          v-model="form.new_password2"
          :placeholder="$t('reset_password_confirm.password_again')"
          type="password"
        >
        <FormFieldValidationError :errors="errors.new_password2" />

        <FormFieldValidationError :errors="errors.other" />
        <button
          type="submit"
          class="btn right"
        >
          {{ $t('reset_password_confirm.reset') }}
        </button>
      </form>
    </div>
  </div>
</template>


<script>
import { api, endpoints, InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'

export default {
  components: {
    FormFieldValidationError,
  },
  data: () => {
    return {
      form: {
        new_password1: null,
        new_password2: null,
      },
      errors: {
        new_password1: [],
        new_password2: [],
        other: [],
      },
    }
  },
  methods: {
    async submit () {
      try {
        const response = await api(
          endpoints.password_reset_confirm(),
          {
            ...this.form,
            uid: this.$route.params.uid,
            token: this.$route.params.token,
          }
        )

        if (!response.ok) {
          throw new InvalidRequestError(
            response.status,
            await response.json()
          )
        } else {
          this.$router.push({name: 'login'})
        }
      } catch (err) {
        console.dir(err.response)
        if (err instanceof InvalidRequestError) {
          this.errors.new_password1 = err.response.new_password1 || []
          this.errors.new_password2 = err.response.new_password2 || []

          if (err.response.uid || err.response.token) {
            this.errors.other = [this.$t('reset_password_confirm.error')]
          }
        } else {
          this.errors.other = [err.message]
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/small_form.scss';
</style>
