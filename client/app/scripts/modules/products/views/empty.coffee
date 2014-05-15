Marionette = require 'backbone.marionette'

module.exports = class EmptyView extends Marionette.ItemView
  template: require './templates/empty'
