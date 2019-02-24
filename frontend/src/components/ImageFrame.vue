<template>
  <img
    :srcset="getSet"
    :src="getLargest.url"
  >
</template>

<script>

export default {
  /* props: {
    files: Array
  },
  */
  data () {
    return {
      files: [
            {
                "url": "http://localhost:8000/media/2_thumbnail.jpg",
                "height": 200,
                "width": 200
            },
            {
                "url": "http://localhost:8000/media/2_small.jpg",
                "height": 400,
                "width": 300
            },
            {
                "url": "http://localhost:8000/media/2_medium.jpg",
                "height": 700,
                "width": 525
            },
            {
                "url": "http://localhost:8000/media/2_large.jpg",
                "height": 1000,
                "width": 750
            }
        ]
    }
  },
  computed: {
    getSet () {
      let srcset = ''
      for (let file of this.files) {
        srcset += `${file.url} ${file.width}w,`
      }
      return srcset
    },
    getLargest () {
      return this.files.map(v => v).sort((a, b) => a.width + b.width)
    }
  }
}
</script>
