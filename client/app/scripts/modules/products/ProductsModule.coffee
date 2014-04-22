module.exports = class ProductsModule extends Marionette.Module
  mainView: require './views/MainView'

  initialize: ->
    @startWithParent = true

  getRegion: ->
    if not @region
      @region = @app.request 'default:region'
    return @region

  onStart: ->
    view = new @mainView
    # The empty view will be shown instead of products list
    @getRegion().show view

    (@app.request 'cardset:entities').done (result) ->
      view.collection = result.objects
      # Rerender view for products list to be shown
      view.render()
