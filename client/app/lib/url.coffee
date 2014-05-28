conf = require '../config'

module.exports = (url) ->
  conf.apiBaseUrl.replace(/([^\/])$/, '$1/') + url.replace(/^\//, '')
