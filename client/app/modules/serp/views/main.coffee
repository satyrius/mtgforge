Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.CompositeView
  template: require './templates/main'
  emptyView: require './empty'
