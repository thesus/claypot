function getCookie(name) {
  const value = "; " + document.cookie
  const parts = value.split("; " + name + "=");
  if (parts.length == 2) {
    return parts.pop().split(";").shift();
  }
  return null
}

function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}

class Timer {
  constructor (func, time = 200) {
    this.timer = setTimeout(func, time)
  }

  clear () {
    clearTimeout(this.timer)
  }
}

/*
 * Removes all properties that are undefined, null or an empty string
 * Returns a (shallow) copy.
*/
function cleanObject(object) {
    const result = {}
    for (const property in object) {
      const value = object[property]
      if (value != undefined && value != null && value != '') {
        result[property] = value
      }
    }
  return result
}

export {
  getCookie,
  clone,
  cleanObject,
  Timer
}
