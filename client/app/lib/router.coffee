Marionette = require 'backbone.marionette'

module.exports = class ReverseRouter extends Marionette.AppRouter
  initialize: (options) ->
    app = options.controller.app
    for name, handler of Marionette.getOption @, 'reverse'
      app.reqres.setHandler "#{name}:uri", handler

