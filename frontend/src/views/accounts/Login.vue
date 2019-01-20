<template>
    <div>
        <div class="login">
            <form @submit.prevent="submit">
                <input type="text" v-model="username" :placeholder="$t('login.username')">
                <input type="password" v-model="password" :placeholder="$t('login.password')">
                <router-link :to="{ name: 'reset-password' }">{{ $t('login.forgot_password') }}</router-link>
                <router-link :to="{ name: 'signup' }">{{ $t('login.signup') }}</router-link>
                <button type="submit" class="btn btn-right">{{ $t('login.login') }}</button>
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
    margin: 2px 8px 0 1px;
}
</style>
