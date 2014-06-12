ApplicationController = require '../../lib/controller'
MainView = require './views/main'

module.exports = class CardsController extends ApplicationController
  showCard: (id) ->
    # Get card and create new view instance
    card = @app.reqres.request 'card:entity', id
    view = new MainView model: card

    # Get region to show card info (main or modal, depends on serp)
    region = @app.reqres.request 'info:region'
    # Navigate back to the last serp (if it was)
    view.on 'show', =>
      region.once 'close', =>
        @app.execute 'last:search:navigate'

    if card.deferred
      card.deferred.done ->
        region.show view
    else
      region.show view