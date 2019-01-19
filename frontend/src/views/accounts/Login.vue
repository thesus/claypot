<template>
    <div>
        <div class="login">
            <form @submit.prevent="submit">
                <input type="text" v-model="username" placeholder="Username">
                <input type="password" v-model="password" placeholder="Password">
                <router-link :to="{ name: 'reset-password' }">Forgot password</router-link>
                <button type="submit" class="btn btn-right">Login</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            username: null,
            password: null
        }
    },
    methods: {
        submit () {
            this.$store.dispatch('login', this.$data)
        }
    }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/small_form.scss';

a {
    float: left;
    font-size: 14px;
    margin: 2px 0 0 1px;
}
</style>
