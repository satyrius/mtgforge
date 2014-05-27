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

      oldHandler = @app.reqres.getHandler 'card:entity'
      # Replace entities get card handler, return models from current
      # collection from a search sesults
      @app.reqres.setHandler 'card:entity', (id) ->
        card = cards.get id
        # Set deferred object to unify card model usage, see cards/controller
        card.deferred = cards.deferred
        return card
      # Restore old gettings card entity handler
      if oldHandler
        view.on 'close', =>
          @app.reqres.setHandler 'card:entity', oldHandler

      # Reset FTS input on close
      view.on 'close', =>
        @app.vent.trigger 'form:reset:fts', ''

      # Show card list view in the result region
      layout.result.show view

  showCardSet: (cardSet) ->
    @listCards set: cardSet
