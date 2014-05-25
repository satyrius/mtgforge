Marionette = require 'backbone.marionette'
MainView = require './views/main'

module.exports = class SearchModule extends Marionette.Module
  onStart: ->
    view = new MainView()
    region = @app.reqres.request 'header:region'
    region.show view

    # Listen to form submit and broadcast event to show search result
    view.on 'search', (fts) =>
      @app.commands.execute 'cards:search', q: fts, true

    # Update fts input when reset broadcast comes
    @app.vent.on 'form:reset:fts', (fts) ->
      view.resetFTS fts
