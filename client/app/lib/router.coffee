Backbone = require 'backbone'
Marionette = require 'backbone.marionette'

module.exports = class ReverseRouter extends Marionette.AppRouter
  getCurrentFragment: (fragment) ->
    Backbone.history.getFragment fragment

  _reverse: (reverser, args) ->
    res = reverser.apply @, args
    @getCurrentFragment res

  initialize: (options) ->
    app = options.controller.app
    for name, handler of Marionette.getOption @, 'reverse'
      do (handler) =>
        app.reqres.setHandler "#{name}:uri", =>
          '#' + @_reverse handler, arguments

        # Navigate to the route without triggering its handler
        app.commands.setHandler "#{name}:navigate", =>
          fragment = @_reverse handler, arguments
          @navigate fragment, {trigger: false}
