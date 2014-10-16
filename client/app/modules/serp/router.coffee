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

  onRoute: ->
    # This is to go back to the previous serp from modal windows
    fragment = @getCurrentFragment()
    app = @_getController().app
    do (app, fragment) =>
      app.commands.setHandler 'last:search:navigate', =>
        @navigate fragment, {trigger: false}
