<template>
  <transition>
    <div class="alert">
      <span class="content">
        <slot></slot>
      </span>
      <span class="close" @click="$emit('close', {})">x</span>
    </div>
  </transition>
</template>

<script>
export default {
  props: {
    timeout: {
      reqired: false,
      default: 10000
    }
  },
  data () {
    return {
      timer: null
    }
  },
  mounted () {
    this.timer = setTimeout(() => {
      this.$emit('close', {})
    }, this.timeout)
  },
  beforeDestroy() {
    clearTimeout(this.timer)
  }
}
</script>

<style lang="scss" scoped>
.alert {
  z-index: 1000;
	position: fixed;
	top: 15px;
	right: 10px;

	width: 300px;
	padding: 5px 5px 5px 11px;

	background-color: #d50e0e;
	color: white;

	border: none;
	border-radius: 3px;

	text-align: left;

  span {
    margin: 3px;
    display: block;
  }

  .content {
    width: 275px;
  }

  .close {
    cursor: pointer;
    float: right;
    position: absolute;
    top: 3px;
    right: 3px;
    width: 20px;
    height: 20px;
    text-align: center;

  }
}
</style>
