conf = require '../config'

module.exports =
  resolveApiUrl: (uri) ->
    unless uri.match /^\/api/
      uri = conf.apiBaseUrl + '/' + uri.replace(/^\//, '')
    return conf.apiHost + uri
