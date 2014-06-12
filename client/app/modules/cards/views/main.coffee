Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.ItemView
  className: 'modal-dialog'
  template: require './templates/main'
