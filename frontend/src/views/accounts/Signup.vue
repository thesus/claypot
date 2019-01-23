<template>
    <div>
        <div class="signup">
            <form @submit.prevent="submit">
                <h5>{{ $t('signup.heading') }}</h5>
                <input type="email" v-model="form.email" :placeholder="$t('signup.email')" :class="{'form-error': !!getErrors.email.length}">
                <form-field-validation-error :errors="getErrors.email" />
                <input type="text" v-model="form.username" :placeholder="$t('signup.username')" :class="{'form-error': !!getErrors.username.length}">
                <form-field-validation-error :errors="getErrors.username" />
                <input type="password" v-model="form.password1" :placeholder="$t('signup.password')" :class="{'form-error': !!getErrors.password1.length}">
                <form-field-validation-error :errors="getErrors.password1" />
                <input type="password" v-model="form.password2" :placeholder="$t('signup.password_again')" :class="{'form-error': !!getErrors.password2.length}">
                <form-field-validation-error :errors="getErrors.password2" />

                <form-field-validation-error :errors="getErrors.other" />

                <p v-if="finished">{{ $t("signup.confirm") }}</p>
                <button type="submit" class="btn btn-right">{{ $t('signup.signup') }}</button>
            </form>
        </div>
    </div>
</template>

<script>
import { api, endpoints,InvalidRequestError } from '@/api'
import FormFieldValidationError from '@/components/FormFieldValidationError'

export default {
    components: {
        FormFieldValidationError
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
            finished: false
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

                ...this.errors
            }
        }
    },
    methods: {
        async submit () {
            try {
                const response = await api(
                    endpoints.signup(),
                    this.$data.form
                )

                if (!response.ok) {
                    throw new InvalidRequestError(
                        response.status,
                        await response.json()
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
