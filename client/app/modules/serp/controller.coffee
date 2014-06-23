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
    reqres = @app.reqres
    # Close modal region immediately for cleanup previous states
    modalRegion.close()
    # Handle showing card in a modal region to add next/prev links
    navHandler = (modalLayout) ->
      modalLayout.body.on 'show', (view) ->
        next = reqres.request 'next:card:entity', view.model
        if next
          next.set 'uri', (reqres.request 'card:uri', next.id)
          modalRegion.setNext next
        prev = reqres.request 'prev:card:entity', view.model
        if prev
          prev.set 'uri', (reqres.request 'card:uri', prev.id)
          modalRegion.setPrev prev
    modalRegion.on 'show', navHandler
    # Back to the last search page on modal close
    backHandler = =>
      @app.execute 'last:search:navigate'
    modalRegion.on 'close', backHandler
    # Remove handlers
    layout.once 'close', ->
      modalRegion.off 'show', navHandler
      modalRegion.off 'close', backHandler

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
