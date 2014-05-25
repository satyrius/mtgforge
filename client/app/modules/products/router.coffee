Router = require '../../lib/router'

module.exports = class ProductsRouter extends Router
  appRoutes:
    'products': 'listProducts'
