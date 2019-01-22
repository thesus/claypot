<template>
    <div>
        <div class="reset-confirm">
            <form @submit.prevent="submit">
                <input blank="false" type="password" v-model="passwords.new_password1" :placeholder="$t('reset_password_confirm.password')">
                <form-field-validation-error :errors="errors.new_password1" />
                <input type="password" v-model="passwords.new_password2" :placeholder="$t('reset_password_confirm.password_again')">
                <form-field-validation-error :errors="errors.new_password2" />

                <form-field-validation-error :errors="errors.other" />
                <button type="submit" class="btn btn-right">{{ $t('reset_password_confirm.reset') }}</button>
            </form>
        </div>
    </div>
</template>


<script>
import { api, endpoints, InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/FormFieldValidationError'

export default {
    components: {
        FormFieldValidationError
    },
    data: () => {
        return {
            passwords: {
                new_password1: null,
                new_password2: null,
            },
            errors: {
                new_password1: [],
                new_password2: [],
                other: []
            }
        }
    },
    methods: {
        async submit () {
            try {
                const response = await api(
                    endpoints.password_reset_confirm(),
                    {
                        ...this.passwords,
                        uid: this.$route.params.uid,
                        token: this.$route.params.token
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
        }
    }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/small_form.scss';
</style>
