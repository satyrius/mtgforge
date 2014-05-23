Marionette = require 'backbone.marionette'
MainView = require './views/main'

module.exports = class SearchModule extends Marionette.Module
  getRegion: ->
    if not @region
      @region = @app.reqres.request('header:region')
    return @region

  onStart: ->
    view = new MainView()
    @getRegion().show view

    # Listen to form submit and broadcast event to show search result
    view.on 'search', (fts) =>
      @app.commands.execute 'cards:search', q: fts, true

    @app.vent.on 'form:reset:fts', (fts) ->
      view.resetFTS fts
