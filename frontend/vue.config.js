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
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false
    }
  }
}
