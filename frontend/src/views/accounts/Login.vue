<template>
    <div>
        <div class="login">
            <form @submit.prevent="submit">
                <input type="text" v-model="username" placeholder="Username">
                <input type="password" v-model="password" placeholder="Password">
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

form {
    @media screen and (min-width: 400px) {
        width: 300px;
        margin: auto;
    }
    width: calc(100% - 20px);
    margin: 10px;
    padding: 5px;
    background-color: white;
    border: solid 1px #ccc;
    box-sizing: border-box;
    display: inline-block;
}
</style>
