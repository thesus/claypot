export default function injectedConfig() {
  const djangoInjectedDataElement = document.getElementById("DID")
  if (djangoInjectedDataElement === null) {
    return {}
  }
  try {
    return JSON.parse(djangoInjectedDataElement.textContent)
  } catch (err) {
    return {}
  }
}
