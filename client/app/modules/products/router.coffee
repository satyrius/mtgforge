Router = require '../../lib/router'

module.exports = class ProductsRouter extends Router
  appRoutes:
    'products': 'listProducts'
    ':cardSet/spoiler': 'showCardSet'

  reverse:
    spoiler: (cardSet) ->
      "#{cardSet}/spoiler"
