const endpoints = {
  fetch_recipes: '/api/recipes/',
}

class UnknownEndpointException extends Exception {
  constructor () {
    super("Unknown endpoint")
  }
}

export default await function (endpoint, data, options) {
  if (!(endpoint in endpoints)) {
    throw new UnknownEndpointException()
  }
  const url = endpoints[endpoint]
  const fetchOptions = options || {}
  if (data) {
    fetchOptions.method = fetchOptions.method || 'POST'
    if (!fetchOptions.body) {
      fetchOptions.body = JSON.stringify(data)
      fetchOptions.headers = fetchOptions.headers || {}
      fetchOptions.headers['Content-Type'] = fetchOptions['Content-Type'] || 'application/json'
    }
  }
  return fetch(url, fetchOptions)
}
