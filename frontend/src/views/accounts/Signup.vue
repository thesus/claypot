<template>
    <div>
        <div class="signup">
            <form @submit.prevent="submit">
                <h5>Signup</h5>
                <input type="email" v-model="email" placeholder="E-Mail Address">
                <input type="text" v-model="username" placeholder="Username">
                <input type="password" v-model="password1" placeholder="Password">
                <input type="password" v-model="password2" placeholder="Password (again)">
                <button type="submit" class="btn btn-right">Signup</button>
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
