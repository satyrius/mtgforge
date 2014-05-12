Router = require './router'
Controller = require './controller'

module.exports = class SerpModule extends Marionette.Module
  initialize: ->
    ctrl = new Controller(app: @app)
    @addInitializer (options) ->
      new Router
        controller: ctrl
