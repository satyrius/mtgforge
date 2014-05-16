ApplicationController = require '../../lib/controller'
MainView = require './views/main'

module.exports = class SerpController extends ApplicationController
  listCards: ->
    @show new MainView()

  showCardSet: (cardSet) ->
    cs = @app.request 'cardset:entity',
      acronym: cardSet
    @show new MainView model: cs
