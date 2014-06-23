Marionette = require 'backbone.marionette'
NavView = require './views/nav'

module.exports = class ModelNavRegion extends Marionette.Region
  show: (model) ->
    view = new NavView
      model: model,
      template: Marionette.getOption @, 'template'
    super view
