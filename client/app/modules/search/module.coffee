Marionette = require 'backbone.marionette'
MainView = require './views/main'

module.exports = class SearchModule extends Marionette.Module
  getRegion: ->
    if not @region
      @region = @app.reqres.request('header:region')
    return @region

  onStart: ->
    view = new MainView()
    view.on 'search', (fts) =>
      @app.trigger 'cards:search', fts
    @getRegion().show view
