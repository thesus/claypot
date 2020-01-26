<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from "@/layout/Navbar"

export default {
  components: {
    Navbar,
  }
}
</script>

<style lang="scss">
@import '@/modules/inputs.scss';
@import '@/modules/variables.scss';

#app {
  font-family: $font_family;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $font_color;

  margin: 50px 10px 10px 10px;
  @media screen and (max-width: 500px) {
    margin-top: 60px;
  }

  @media screen and (min-width: 1000px) {
    width: 80%;
    margin: 50px auto auto auto;
  }
}

body {
    margin: 0;
}

h3, h4, h5, h6 {
    margin: 2px 0 5px 0;
}

a {
  display: inline-block;
}

ol {
  padding: 0;
}


@media print {
  body, div {
    background-color: transparent !important;
  }

  #app {
    margin-top: 0;
  }

  .nav, div.functions, div.relations, .btn {
    display: none !important;
  }

  div.information {
    border: none !important;
  }

  h1 {
    text-align: left;
    margin: 5px 0 0 0 !important;
  }

  .ingredients-group {
    width: 180px !important;
  }
}


</style>
