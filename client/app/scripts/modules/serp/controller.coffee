module.exports = class SerpController extends Marionette.Controller
  mainView: require './views/main'

  initialize: (options) ->
    @app = options.app

  getRegion: ->
    if not @region
      @region = @app.request 'default:region'
    return @region

  listCards: ->
    console.log 'serp'
    view = new @mainView
    @getRegion().show view
