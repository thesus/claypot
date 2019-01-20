import { getCookie } from '@/utils'

const endpoints = {
  fetch_csrf_token () {
    return '/api/csrf'
  },
  fetch_recipes () {
    return '/api/recipes/'
  },
  fetch_recipe (id) {
    return `/api/recipes/${id}/`
  },
  login () {
    return '/accounts/login'
  },
  logout () {
    return '/accounts/logout'
  },
  password_reset () {
    return '/accounts/reset'
  },
  password_reset_confirm () {
    return '/accounts/confirm'
  },
  signup () {
    return '/accounts/signup'
  },
  post_recipe (id) {
    if (id) {
      return `/api/recipes/${id}/`
    } else {
      return '/api/recipes/'
    }
  },
}

for (let [e, f] of Object.entries(endpoints)) {
  endpoints[e] = function () {
    return {
      earmarked: 1,
      url: f(...arguments),
    }
  }
}

class UnknownEndpointError extends Error {
  constructor () {
    super("Unknown endpoint")
  }
}

function _needsCsrfToken(method) {
  switch (method.toLowerCase()) {
    case 'head':
    case 'get':
    case 'options':
      // make absolutely sure these methods do not alter data
      return false
    default:
      return true
  }
}

async function api(endpoint, data, options) {
  if (!endpoint.earmarked) {
    throw new UnknownEndpointError()
  }
  const url = endpoint.url
  const fetchOptions = options || {}
  fetchOptions.credentials = fetchOptions.credentials || 'same-origin'

  if (data) {
    fetchOptions.method = fetchOptions.method || 'POST'

    if (!fetchOptions.body) {
      fetchOptions.body = JSON.stringify(data)
      fetchOptions.headers = fetchOptions.headers || {}
      fetchOptions.headers['Content-Type'] = fetchOptions['Content-Type'] || 'application/json'
    }

    fetchOptions.needsCsrfToken = fetchOptions.needsCsrfToken || _needsCsrfToken(fetchOptions.method)
    let csrf = getCookie('csrftoken')
    if (!csrf) {
      if (fetchOptions.needsCsrfToken) {
        await api(endpoints.fetch_csrf_token())
        csrf = getCookie('csrftoken')
      }
    }

    if (fetchOptions.needsCsrfToken && csrf) {
      fetchOptions.headers['X-CSRFToken'] = csrf
    }

  }
  return fetch(url, fetchOptions)
}

export { api, endpoints }
