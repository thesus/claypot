/* Unit tests designed to find errors in localization.
 * The actual tests are generated by code to easily ensure all
 * locales are compared to each other.
 *
 * Unfortunately we cannot use `request.context` here - which is how
 * all locales are loaded in the main appliation. If we try to use that
 * function, jest tells us, that it is undefined and some Internet search
 * reveals, that this function is simply not supported. We deal with this
 * by manually adding new locales in two places to test them.
 *
 * How to add a new locale:
 * 1. Import your new locale at [MARKER1].
 * 2. Add your locale to Map at [MARKER2].
 * 3. Done.
 */

// [MARKER1] Import all locales
import locale_en from '@/locales/en'
import locale_de from '@/locales/de'

/* [MARKER2] List of locales. They are compared to each other.
 * The key is just a name, but it has be unique. The value is the
 * actual locales object.
 */
const knownLocales = new Map([
  ['en', locale_en],
  ['de', locale_de],
])

/* creates a Set from obj, that contains just the keys.
 * If a value is a sub-object, it contains an array with two
 * elements: that keys name and a set of that objects keys.
 * This data structure is used to recursively find missing keys
 * in objects.
 *
 * Example:
 *
 * Input: {key1: "...", key2: {subkey1: "..."}}
 *
 * Output: Set {
 *  "key1",
 *  [
 *    "key2": Set {
 *      "subkey1"
 *    }
 *  ]
 * }
 */
function settify (obj) {
  const result = new Set()
  const keys = Object.keys(obj)
  for (const key of keys) {
    const value = obj[key]
    if (typeof value === 'object') {
      result.add([key, settify(value)])
    } else {
      result.add(key)
    }
  }
  return result
}

/* subtracts data structures as returned from `settify`.
 * This is used to find the difference between two data structures.
 * If two data structures contain the same elements, the result is
 * an empty set.
 *
 * Example:
 *
 * Input 1: Set {
 *  "key1",
 *  "extra-key1",
 *  [
 *    "key2",
 *    Set {
 *      "subkey1",
 *      "extra-subkey1"
 *    }
 *  ]
 * }
 * Input 2: Set {
 *  "key1",
 *  [
 *    "key2",
 *    Set {
 *      "subkey1",
 *    }
 *  ]
 * }
 *
 * Result: Set {
 *  "extra-key1",
 *  [
 *    "key2",
 *    Set {
 *      "extra-subkey1"
 *    }
 *  ]
 * }
 */
function subtract (set1, set2) {
  const result = new Set()
  for (const item of set1.values()) {
    if (typeof item === 'object') {
      // case for nested keys
      // find corresponding item in set2:
      let found = false
      for (const item2 of set2.values()) {
        if (typeof item2 === 'object' && item2[0] === item[0]) {
          found = true
          const subtraction = subtract(item[1], item2[1])
          if (subtraction.size > 0) {
            result.add([item[0], subtraction])
          }
        }
      }
      if (!found) {
        result.add(item)
      }
    } else {
      // case for normal keys
      if (!set2.has(item)) {
        result.add(item)
      }
    }
  }
  return result
}

// helper data structures
const settifyiedLocales = new Map()
for (const [id, locale] of knownLocales) {
  settifyiedLocales.set(id, settify(locale))
}
const emptySet = new Set()

// generated tests for each locale
for (const [id, settifiedLocale] of settifyiedLocales) {
  describe(`locale ${id}`, () => {
    for (const [id2, settifiedLocale2] of settifyiedLocales) {
      if (id === id2) {
        // locales are not compared to themselfs.
        continue
      }
      it(`has all keys from ${id2}`, () => {
        expect(subtract(settifiedLocale2, settifiedLocale)).toMatchObject(emptySet)
      })
    }
  })
}
