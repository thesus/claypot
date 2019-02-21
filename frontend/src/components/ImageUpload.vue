<template>
  <form enctype="multipart/form-data" v-on:submit.prevent="submitImages">
    <label class="input">
      <span class="btn btn-default">Select images</span>
      <input
        type="file"
        multiple
        ref="input"
        accept="image/*"
        @change="selectImages">
    </label>
    <button class="btn btn-default btn-right" type="submit">Submit</button>
  </form>
</template>

<script>
import { api, endpoints, InvalidRequestError } from '@/api'

export default {
  data () {
    return {
      'images': []
    }
  },
  methods: {
    selectImages (event) {
      /* Clear existing images */
      this.images = []
      const images = this.$refs.input.files

      for (let image of images) {
        this.images.push({
          'file': image,
          'success': false
        })
      }
    },
    submitImages () {
      for (let image of this.images) {
        if (image.succes !== true) {
          this.uploadImage(image)
        }
      }
    },
    async uploadImage (image) {
      let data = new FormData()
      console.log(image)
      data.append('image', image.file)

      const options = {
        'body': data,
        'method': 'post'
      }

      const response = await api(
        endpoints.upload_image(),
        null,
        options
      )

      if (response.ok) {
        console.log('yay')
      } else {
        console.log(await response.json())
      }
    }
  }
}
</script>

<style lang="scss" scoped>
input[type=file] {
  display: none;
  overflow: hidden;
  position: relative;
}
</style>
