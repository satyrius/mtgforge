Marionette = require 'backbone.marionette'

module.exports = class CardView extends Marionette.ItemView
  className: 'td-card'
  template: require './templates/card'
