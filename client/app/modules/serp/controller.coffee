_ = require 'underscore'
qs = require 'qs'
ApplicationController = require '../../lib/controller'
MainView = require './views/main'
ResultView = require './views/result'

module.exports = class SerpController extends ApplicationController
  listCards: (query) ->
    layout = new MainView()
    @show layout

    if _.isString query
      query = qs.parse query
    @app.vent.trigger 'form:reset:fts', query.q

    cards = @app.request('card:entities', query)
    cards.deferred.done =>
      view = new ResultView
        collection: cards

      # Reset FTS input on close
      view.on 'close', =>
        @app.vent.trigger 'form:reset:fts', ''

      # Show card list view in the result region
      layout.result.show view

  showCardSet: (cardSet) ->
    @listCards set: cardSet
