import { getCookie } from '@/utils'

const endpoints = {
  create_many_ingredients () {
    return '/api/ingredients/create_many/'
  },
  check_new_ingredients () {
    return '/api/ingredients/check_new/'
  },
  fetch_csrf_token () {
    return '/api/csrf'
  },
  fetch_sentry_config () {
    return '/api/sentry'
  },
  fetch_recipes () {
    return '/api/recipes/'
  },
  fetch_recipe (id) {
    return `/api/recipes/${id}/`
  },
  fetch_ingredient (id) {
    return `/api/ingredients/${id}/`
  },
  fetch_ingredients () {
    return '/api/ingredients/'
  },
  fetch_recipe_relation (id) {
    if (id) {
      return `/api/recipe_relations/${id}/`
    } else {
      return '/api/recipe_relations/'
    }
  },
  fetch_user (id) {
    return `/api/accounts/users/${id}/`
  },
  login () {
    return '/api/accounts/login/'
  },
  logout () {
    return '/api/accounts/logout/'
  },
  password_reset () {
    return '/api/accounts/reset/'
  },
  password_reset_confirm () {
    return '/api/accounts/reset_confirm/'
  },
  recipe_star (id) {
    return `/api/recipes/${id}/star/`
  },
  recipe_unstar (id) {
    return `/api/recipes/${id}/unstar/`
  },
  fork (id) {
    return `/api/recipes/${id}/fork/`
  },
  signup () {
    return '/api/accounts/signup/'
  },
  post_recipe (id) {
    if (id) {
      return `/api/recipes/${id}/`
    } else {
      return '/api/recipes/'
    }
  },
  recipe_draft (id) {
    return id ? `/api/drafts/${id}/` : '/api/drafts/'
  },
  search_ingredients (term) {
    term = encodeURIComponent(term)
    return `/api/ingredients/?name=${term}&page_size=5`
  },
  upload_image () {
    return '/api/images/'
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

class InvalidRequestError extends Error {
  constructor (code, response) {
    super("Request resulted in an error.")
    this.code = code
    this.response = response
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

  let url = endpoint.url
  const fetchOptions = options || {}
  fetchOptions.credentials = fetchOptions.credentials || 'same-origin'
  fetchOptions.headers = fetchOptions.headers || {}

  if (data) {
    fetchOptions.method = fetchOptions.method || 'POST'

    if (!fetchOptions.body && fetchOptions.method.toLowerCase() !== 'head' && fetchOptions.method.toLowerCase() !== 'get') {
      fetchOptions.body = JSON.stringify(data)
      fetchOptions.headers['Content-Type'] = fetchOptions['Content-Type'] || 'application/json'
    } else if (Object.keys(data).length > 0) {
      url += "?" + Object.entries(data).map(([k, v]) => `${encodeURI(k)}=${encodeURI(v)}`).join('&')
    }
  }
  fetchOptions.method = fetchOptions.method || 'GET'

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
  return fetch(url, fetchOptions)
}

export { api, endpoints, InvalidRequestError }
