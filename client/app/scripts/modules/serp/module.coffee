Router = require './router'
Controller = require './controller'

module.exports = class SerpModule extends Marionette.Module
  initialize: ->
    @startWithParent = true

    ctrl = new Controller(app: @app)
    @addInitializer (options) ->
      new Router
        controller: ctrl
