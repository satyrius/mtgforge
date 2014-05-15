Marionette = require 'backbone.marionette'

module.exports = class ApplicationController extends Marionette.Controller
  initialize: (options) ->
    @app = options.app

  getRegion: ->
    if not @region
      @region = @app.request 'default:region'
    return @region

  show: (view) ->
    @getRegion().show view
