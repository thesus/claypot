<template>
    <div>
        <div class="login">
            <form @submit.prevent="submit">
                <input autofocus ref="username_input" type="text" v-model="credentials.username" :placeholder="$t('login.username')" :class="{'form-error': !!errors.username.length}">
                <form-field-validation-error :errors="errors.username" />
                <input type="password" v-model="credentials.password" :placeholder="$t('login.password')"  :class="{'form-error': !!errors.password.length}">
                <form-field-validation-error :errors="errors.password" />

                <form-field-validation-error :errors="errors.other" />
                <router-link tabindex="-1" :to="{ name: 'reset-password' }">{{ $t('login.forgot_password') }}</router-link>
                <router-link tabindex="-1" :to="{ name: 'signup' }">{{ $t('login.signup') }}</router-link>
                <button type="submit" class="btn btn-right">{{ $t('login.login') }}</button>
            </form>
        </div>
    </div>
</template>

<script>
import { InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/FormFieldValidationError'

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
                other: []
            }
        }
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
    mounted () {
        this.$refs.username_input.focus()
    }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/small_form.scss';

a {
    float: left;
    font-size: 14px;
    margin: 2px 8px 0 1px;
}
</style>
