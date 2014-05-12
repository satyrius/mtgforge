module.exports = class SearchModule extends Marionette.Module
  mainView: require './views/main'

  getRegion: ->
    if not @region
      @region = @app.reqres.request('header:region')
    return @region

  onStart: ->
    @getRegion().show new @mainView()
