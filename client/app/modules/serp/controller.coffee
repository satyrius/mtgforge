_ = require 'underscore'
qs = require 'qs'
ApplicationController = require '../../lib/controller'
MainView = require './views/main'
ResultView = require './views/result'

module.exports = class SerpController extends ApplicationController
  listCards: (query) ->
    layout = new MainView()
    @show layout

    # Modal region to show card info
    modalRegion = @app.getRegion('modal')
    # Close modal region immediately for cleanup previous states
    modalRegion.close()

    if _.isString query
      query = qs.parse query
    @app.vent.trigger 'form:reset:fts', query.q

    cards = @app.request('card:entities', query)
    cards.deferred.done =>
      view = new ResultView
        collection: cards

      # Replace default info region with modal region to show card info
      infoRegion = @app.request 'info:region'
      view.on 'show', =>
        @app.reqres.setHandler 'info:region', -> modalRegion
      view.on 'close', =>
        @app.reqres.setHandler 'info:region', -> infoRegion

      # Reset FTS input on close
      view.on 'close', =>
        @app.vent.trigger 'form:reset:fts', ''

      # Show card list view in the result region
      layout.result.show view

  showCardSet: (cardSet) ->
    @listCards set: cardSet
