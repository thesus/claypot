<template>
  <div>
    <div class="reset">
      <form @submit.prevent="submit">
        <h5>{{ $t('reset_password.heading') }}</h5>
        <input
          v-model="email"
          :placeholder="$t('reset_password.email')"
          required
          type="email"
        >
        <FormFieldValidationError :errors="errors" />

        <p v-if="finished && errors.length === 0">
          {{ $t('reset_password.confirm') }}
        </p>

        <button
          :disabled="finished && !errors"
          type="submit"
          class="btn right"
        >
          {{ $t('reset_password.reset') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

import { api, endpoints } from '@/api'
import FormFieldValidationError from '@/components/utils/FormFieldValidationError'

export default {
  components: {
    FormFieldValidationError,
  },
  data: () => {
    return {
      finished: false,
      email: null,
      errors: [],
    }
  },
  mounted () {
    this.updateTitle({name: "titles.accounts.reset-password"})
  },
  methods: {
    async submit () {
      try {
        /* Clear errors and status from previous attempts */
        this.finished = false
        this.errors.splice(0)

        await api(
          endpoints.password_reset(),
          {
            email: this.email,
          }
        )

        /* this.$router.push({name: 'home'}) */
      } catch (err) {
        this.errors = [err.message]
      } finally {
        this.finished = true
      }
    },
    ...mapActions(["updateTitle"]),
  },
}
</script>

<style lang="scss" scoped>
@import '@/modules/small_form.scss';

p {
    margin: 0;
}
</style>
