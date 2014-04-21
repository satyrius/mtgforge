module.exports = class ProductsModule extends Marionette.Module
  mainView: require './views/MainView'

  initialize: ->
    @startWithParent = true

  getRegion: ->
    if not @region
      @region = @app.request('default:region')
    return @region

  onStart: ->
    view = new @mainView
      collection: @app.request('cardset:entities')

    @getRegion().show view
