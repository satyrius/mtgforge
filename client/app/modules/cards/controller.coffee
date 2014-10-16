ApplicationController = require '../../lib/controller'
MainView = require './views/main'

module.exports = class CardsController extends ApplicationController
  showCard: (id) ->
    # Get region to show card info (main or modal, depends on serp)
    region = @app.reqres.request 'info:region'

    # Get deferred card model and show info when it's load will be done
    deferred = @app.reqres.request 'card:entity', id
    deferred.done (card) =>
      region.show new MainView model: card
      @app.vent.trigger 'show:card', card
