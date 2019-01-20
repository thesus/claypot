<template>
    <div>
        <div class="signup">
            <form @submit.prevent="submit">
                <h5>{{ $t('signup.heading') }}</h5>
                <input type="email" v-model="email" :placeholder="$t('signup.email')">
                <input type="text" v-model="username" :placeholder="$t('signup.username')">
                <input type="password" v-model="password1" :placeholder="$t('signup.password')">
                <input type="password" v-model="password2" :placeholder="$t('signup.password_again')">
                <button type="submit" class="btn btn-right">{{ $t('signup.signup') }}</button>
            </form>
        </div>
    </div>
</template>

<script>
import { api, endpoints } from '@/api'

export default {
    data: () => {
        return {
            username: null,
            email: null,
            password1: null,
            password2: null
        }
    },
    methods: {
        async submit () {
            try {
                await api(
                    endpoints.signup(),
                    this.$data
                )

            } catch (err) {
                console.log(err)
            }
        }
    }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/small_form.scss';
</style>
