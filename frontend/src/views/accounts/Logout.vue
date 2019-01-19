<template>
    <div>
        You're logged out.
        <router-link :to="{ name: 'home' }">Home</router-link>
    </div>
</template>

<script>
export default {
    mounted() {
        this.$store.dispatch('logout')
    }
}
</script>
