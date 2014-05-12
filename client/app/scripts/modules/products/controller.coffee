ApplicationController = require '../../controller'

module.exports = class ProductsController extends ApplicationController
  mainView: require './views/main'

  listProducts: ->
    (@app.request 'cardset:entities').done (result) =>
      @show new @mainView
        collection: result.collection
