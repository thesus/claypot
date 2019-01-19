<template>
  <div id="app">
    <navigation />
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar"

export default {
    components: {
        'navigation': Navbar
    }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

body {
    margin: 0;
}
</style>
