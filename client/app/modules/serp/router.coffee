qs = require 'qs'
Router = require '../../lib/router'

module.exports = class SerpRouter extends Router
  appRoutes:
    'search?:params': 'listCards'
    'cat/:cardSet': 'showCardSet'

  reverse:
    search: (query) ->
      "search?#{qs.stringify query}"

    spoiler: (cardSet) ->
      "cat/#{cardSet}"
