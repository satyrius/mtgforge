Marionette = require 'backbone.marionette'

module.exports = class ReverseRouter extends Marionette.AppRouter
  initialize: (options) ->
    app = options.controller.app
    for name, handler of Marionette.getOption @, 'reverse'
      do (handler) =>
        app.reqres.setHandler "#{name}:uri", =>
          "#/#{handler.apply @, arguments}"

        # Navigate to the route without triggering its handler
        app.commands.setHandler "#{name}:navigate", =>
          console.log 'nav', name, handler
          # IMPORTANT It should be without leading slash
          fragment = handler.apply @, arguments
          @navigate fragment, {trigger: false}
