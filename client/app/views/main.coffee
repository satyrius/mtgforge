Marionette = require 'backbone.marionette'

module.exports = class AppView extends Marionette.Layout
  template: require './templates/app'
  el: "#app"
