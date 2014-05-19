SpinnerView = require './spinner'
Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.Layout
  template: require './templates/main'

  regions:
    info: '#td-serp-info'
    cards: '#td-serp-cards'
    spinner: '#td-serp-spinner'

  onShow: ->
    @spinner.show new SpinnerView()
