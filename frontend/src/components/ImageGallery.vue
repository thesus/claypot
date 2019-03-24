<template>
  <div class="gallery">
    <div class="control">
      <button
        class="btn"
        :disabled="!hasPrev"
        @click="current--"
      >
        Prev
      </button>
      <button
        class="btn"
        :disabled="!hasNext"
        @click="current++"
      >
        Next
      </button>
    </div>
    <ImageFrame :files="getCurrentImage" />
  </div>
</template>

<script>
import ImageFrame from '@/components/ImageFrame'

export default {
  components: {
    ImageFrame
  },
  props: {
    images: {
      type: Array,
      default () { return [] }
    }
  },
  data () {
    return {
      current: 0
    }
  },
  computed: {
    getCurrentImage () {
      if (this.current < this.images.length) {
        return this.images[this.current]['files']
      } else {
        return []
      }
    },
    hasNext () {
      return this.current + 1 < this.images.length
    },
    hasPrev () {
      return this.current > 0
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';

.gallery {
  position: relative;
  width: 100%;
  height: 100%;
}

.control {
  position: absolute;
  display: flex;
  justify-content: space-between;
  background: transparent;
  width: 100%;
  top: 0;

  .btn {
    margin: 5px;
  }
}
</style>
