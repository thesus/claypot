import { getCookie } from '@/utils'

const endpoints = {
  fetch_recipes () {
    return '/api/recipes/'
  },
  fetch_recipe (id) {
    return `/api/recipes/${id}/`
  },
  login () {
    return '/accounts/login'
  }
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

function api(endpoint, data, options) {
  if (!endpoint.earmarked) {
    throw new UnknownEndpointError()
  }
  const url = endpoint.url
  const fetchOptions = options || {}

  if (data) {
    fetchOptions.method = fetchOptions.method || 'POST'

    if (!fetchOptions.body) {
      fetchOptions.body = JSON.stringify(data)
      fetchOptions.headers = fetchOptions.headers || {}
      fetchOptions.headers['Content-Type'] = fetchOptions['Content-Type'] || 'application/json'
    }

    const csrf = getCookie('csrftoken')
    if (csrf) {
      fetchOptions.headers['X-CSRFToken'] = csrf
    }

  }
  return fetch(url, fetchOptions)
}

export { api, endpoints }
