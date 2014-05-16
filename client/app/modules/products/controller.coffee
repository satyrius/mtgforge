ApplicationController = require '../../lib/controller'

module.exports = class ProductsController extends ApplicationController
  mainView: require './views/main'

  listProducts: ->
    collection = @app.request 'cardset:entities'
    collection.deferred.done () =>
      @show new @mainView
        collection: collection
