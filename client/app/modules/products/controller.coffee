ApplicationController = require '../../lib/controller'
MainView = require './views/main'

module.exports = class ProductsController extends ApplicationController
  listProducts: ->
    # TODO check for Marionette native way to manage view
    if @view then @show @view else
      collection = @app.request 'cardset:entities'
      collection.deferred.done () =>
        @view = new MainView collection: collection
        @show @view
