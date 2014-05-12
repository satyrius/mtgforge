module.exports = class ProductsModule extends Marionette.Module
  mainView: require './views/main'

  initialize: ->
    @startWithParent = true

  getRegion: ->
    if not @region
      @region = @app.request 'default:region'
    return @region

  onStart: ->
    (@app.request 'cardset:entities').done (result) =>
      view = new @mainView
        collection: result.collection
      @getRegion().show view
