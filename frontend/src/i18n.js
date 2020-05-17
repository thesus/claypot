import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

function loadLocaleMessages () {
  const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
  const messages = {}
  locales.keys().forEach(key => {
    const matched = key.match(/([A-Za-z0-9-_]+)\./i)
    if (matched && matched.length > 1) {
      const locale = matched[1]
      messages[locale] = locales(key)
    }
  })
  return messages
}

let locale = 'en'  // initialized to fallback value
const messages = loadLocaleMessages()

/* Note: This has a weakness, that is not relevant now, but might be at
 * some point. We will not properly handle specific available locales.
 * E. g. we will not pass out an available "en-gb", when a user requests
 * a more generic "en", but we have no generic "en" available.
 */
const availableLanguages = new Set(Object.keys(messages).map(i => i.toLowerCase()))

/* find the preferred language of the user. We do so by looking through
 * the languages the user likes and then prefering any verison of that
 * language we have over other languages the user likes. Better matches
 * are prefered to more loose matches, e. g. an available "en-gb" locale
 * would be prefered over a generic "en" locale.
 *
 * Note that this means if a user informas us, they would like the languages
 * ["en-us", "de", "en"], we will look for "en-us" first, then *any* "en" locale,
 * then for "de" and then for "en".
 *
 * We only support "xx-xx" and "xx" format, not the whole BCP47.
 */
findLangLoop:
  for (const preferredLanguage of navigator.languages) {
    const langParts = preferredLanguage.toLowerCase().split('-')
    // looking for increasingly more generic version of language
    for (let i = langParts.length; i >= 1; i--) {
      const lookFor = langParts.slice(0, i).join('-')
      if (availableLanguages.has(lookFor)) {
        locale = lookFor
        break findLangLoop
      }
    }
  }

export default new VueI18n({
  locale: locale,
  fallbackLocale: process.env.VUE_APP_I18N_FALLBACK_LOCALE || 'en',
  messages
})
