qs = require 'qs'
Router = require '../../lib/router'

module.exports = class SerpRouter extends Router
  appRoutes:
    'search?:params': 'listCards'

  reverse:
    search: (query) ->
      "search?#{qs.stringify query}"
