Marionette = require 'backbone.marionette'

module.exports = class NavView extends Marionette.ItemView
  initialize: (options) ->
    @template = options.template
