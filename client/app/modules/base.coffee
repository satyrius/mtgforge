Marionette = require 'backbone.marionette'

module.exports = class BaseModule extends Marionette.Module
  initialize: ->
    ctrl = new @Controller
      app: @app
    @addInitializer (options) ->
      @router = new @Router
        controller: ctrl
