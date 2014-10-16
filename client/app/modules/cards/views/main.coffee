Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.ItemView
  className: 'container-fluid'
  template: require './templates/main'
