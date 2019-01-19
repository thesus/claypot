<template>
    <div>
        <div class="login">
            <form @submit.prevent="submit">
                <input type="text" v-model="username" placeholder="Username">
                <input type="password" v-model="password" placeholder="Password">
                <button type="submit" class="btn">Login</button>
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

</style>
