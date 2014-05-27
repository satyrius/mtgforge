ApplicationController = require '../../lib/controller'
MainView = require './views/main'

module.exports = class CardsController extends ApplicationController
  showCard: (id) ->
    region = @app.reqres.request 'info:region'
    card = @app.reqres.request 'card:entity', id
    card.deferred.done ->
      region.show new MainView model: card
