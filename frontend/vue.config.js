module.exports = {
  chainWebpack: config => {
    config.resolve
      .extensions
        .prepend('.mjs')

    config.module
      .rule('mjs')
        .test(/\.mjs$/)
        .include
          .add(/node_modules/)
          .end()
        .type('javascript/auto')
  },
  pluginOptions: {
    i18n: {
      // there used to be more configuration for vue-i18n here, but it is handled in src/i18n.js now.

      // this option is not actually from vue-i18n, but from vue-cli-plugin-i18n. They
      // are not really saying, what it is for. I don't see a difference, when changing the value.
      // But since we have to keep the `i18n` key in pluginOptions anyways, because otherwise
      // vue-cli-plugin-i18n breaks the build process, I'll just cargo-cult this.
      enableInSFC: true
    }
  }
}
