Marionette = require 'backbone.marionette'

module.exports = class ProductView extends Marionette.ItemView
  tagName: 'h4'
  template: require './templates/product'
