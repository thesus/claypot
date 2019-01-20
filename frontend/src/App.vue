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
@import '@/modules/variables.scss';

#app {
  font-family: $font_family;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $font_color;
}

body {
    margin: 0;
}

h3, h4, h5, h6 {
    margin: 2px 0 5px 0;
}
</style>
