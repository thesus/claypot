<template>
    <div class="nav">
        <router-link :to="{ name: 'home' }">{{ $t('navbar.home') }}</router-link>
        <router-link v-if="$store.getters.isLoggedIn" :to="{ name: 'logout' }">{{ $t('navbar.logout') }}</router-link>
        <router-link v-else :to="{ name: 'login' }">{{ $t('navbar.login') }}</router-link>
    </div>
</template>

<style lang="scss" scoped>
$border_color: #ddd;

.nav {
    margin: 5px 5px 5px 5px;
    // border-bottom: solid 1px $border_color;
    // border-top: solid 1px $border_color;
}

a {
    margin: 8px 5px 5px 5px;
    display: inline-block;
    color: #2c3e50;
    text-decoration: none;
}

.router-link-exact-active {
    text-decoration: underline;
}
</style>
