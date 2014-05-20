ApplicationController = require '../../lib/controller'
MainView = require './views/main'
ResultView = require './views/result'

module.exports = class SerpController extends ApplicationController
  listCards: ->
    @show new MainView()

  showCardSet: (cardSet) ->
    layout = new MainView()
    @show layout
    cards = @app.request 'card:entities:by_set', cardSet
    cards.deferred.done ->
      view = new ResultView
        collection: cards
      layout.result.show view
      layout.spinner.close()
