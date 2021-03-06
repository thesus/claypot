<template>
  <form
    enctype="multipart/form-data"
    @submit.prevent="submitImages"
  >
    <button
      class="btn"
      @click="openInput"
    >
      {{ $t('image_upload.upload_button') }}
    </button>
    <input
      ref="input"
      type="file"
      multiple
      accept="image/*"
      @change="imageChange"
    >
    <div
      v-if="images"
      class="list"
    >
      <div
        v-for="(image, index) in images"
        :key="index"
        class="thumbnail"
      >
        <span
          class="delete"
          @click="removeImage(index)"
        >{{ $t('image_upload.delete_button') }}</span>
        <img
          :src="image.url"
          :class="{
            'loading': (image.success === null),
            'success': (image.success),
            'failure': (image.success === false)
          }"
        >
      </div>
    </div>
    <span
      v-if="isFailed"
      class="btn"
      @click="submitImages"
    >{{ $t('image_upload.retry_button') }}</span>
  </form>
</template>

<script>
import { api, endpoints, InvalidRequestError } from '@/api'

export default {
  props: {
    initial: {
      type: Array,
      default: () => [],
    }
  },
  data () {
    return {
      'images': [],
    }
  },
  computed: {
    isFailed () {
      return !!this.images.filter(image => image.success === false).length
    },
  },
  watch: {
    initial: {
      handler() {
        /* Add already existing images to stock */
        for (const image of this.initial) {
          this.images.push({
            'success': true,
            'url': image.files[0]['image_file'], // Thumbnail
            'id': image.id
          })
        }

        this.update()
      },
      immediate: true
    }
  },
  methods: {
    update () {
      /* Could update with watch but that's more specific. */
      this.$emit('input', this.images.filter(image => image.success === true).map(image => image.id))
    },
    openInput () {
      this.$refs.input.click()
    },
    removeImage (id) {
      this.$delete(this.images, id)

      this.update()
    },
    imageChange (event) {
      const images = this.$refs.input.files

      for (let image of images) {
        this.images.push({
          'file': image,
          'url': URL.createObjectURL(image),
          'id': null,
          'success': null,
        })
      }

      /* Auto submit and send ids to parent component. */
      this.submitImages()
    },
    async submitImages () {
      const promises = []

      for (let image of this.images) {
        if (image.success !== true) {
          image.success = null
          promises.push(this.uploadImage(image))
        }
      }

      await Promise.all(promises)
      this.update()
    },
    async uploadImage (image) {
      let data = new FormData()
      data.append('image', image.file)

      const options = {
        'body': data,
        'method': 'post'
      }

      try {
        const response = await api(
          endpoints.upload_image(),
          null,
          options,
        )

        if (response.ok) {
          image.success = true
          image.id = (await response.json()).id
        } else {
          // TODO: Add proper error handling
          throw Exception(await response.json())
        }
      } catch (e) {
        image.success = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>

$thumbnail-size: 100px;

input[type=file] {
  display: none;
  overflow: hidden;
  position: relative;
}

.list {
  display: flex;
  justify-content: center;
  flex-flow: row wrap;

  width: 100%;
  margin-top: 4px;
}

.thumbnail {
  width: $thumbnail-size;
  height: $thumbnail-size;
  position: relative;
  display: block;
  margin: 4px;

  .delete {
    display: none;
    background-color: white;
    position: absolute;
    top: 2px;
    left: 2px;
    right: 2px;
    z-index: 1000;
    cursor: pointer;
  }

  /* Show delete option only on hover */
  &:hover {
    .delete {
      display: block;
    }
  }
}


img {
  height: 100%;
  width: 100%;
  object-fit: cover;
  box-sizing: border-box;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  &.loading {
    filter: blur(1px);
  }

  &.success {
    border: 2px solid green;
  }

  &.failure {
    border: 2px solid red;
  }
}

span.btn {
  display: table-cell;
  vertical-align: middle;
}
</style>
