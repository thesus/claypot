<template>
  <img
    :srcset="getSet"
    :src="getLargest.url"
  >
</template>

<script>

export default {
  props: {
    files: {
      type: Array,
      default () { return [] }
    }
  },
  computed: {
    getSet () {
      let srcset = ''
      for (let file of this.files) {
        srcset += `${file.image_file} ${file.width}w,`
      }
      return srcset
    },
    getLargest () {
      return this.files.map(v => v).sort((a, b) => a.width + b.width)
    }
  }
}
</script>

<style lang="scss" scoped>
img {
  width: 100%;
  height: 100%;

  object-fit: cover;
}
</style>
