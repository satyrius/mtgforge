Marionette = require 'backbone.marionette'

module.exports = class ProductsRouter extends Marionette.AppRouter
  appRoutes:
    'products': 'listProducts'
