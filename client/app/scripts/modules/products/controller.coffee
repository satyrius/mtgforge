module.exports = class ProductsController extends Marionette.Controller
  mainView: require './views/main'

  initialize: (options) ->
    @app = options.app

  getRegion: ->
    if not @region
      @region = @app.request 'default:region'
    return @region

  listProducts: ->
    (@app.request 'cardset:entities').done (result) =>
      view = new @mainView
        collection: result.collection
      @getRegion().show view
