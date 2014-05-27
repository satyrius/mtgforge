Router = require '../../lib/router'

module.exports = class CardsRouter extends Router
  appRoutes:
    'card/:id': 'showCard'

  reverse:
    card: (id) ->
      "card/#{id}"
