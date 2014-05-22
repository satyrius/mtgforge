ApplicationController = require '../../lib/controller'
MainView = require './views/main'
ResultView = require './views/result'

module.exports = class SerpController extends ApplicationController
  listCards: ->
    @show new MainView()

  showCards: (cards) ->
    layout = new MainView()
    @show layout
    cards.deferred.done ->
      view = new ResultView
        collection: cards
      layout.result.show view

  showCardSet: (cardSet) ->
    @showCards @app.request('card:entities:by_set', cardSet)

  searchCards: (fts) ->
    @showCards @app.request('card:entities:fts', fts)
