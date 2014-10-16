SpinnerView = require './spinner'
Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.Layout
  template: require './templates/main'

  regions:
    result: '#td-serp-cards'
    spinner: '#td-serp-spinner'

  initialize: ->
    @result.on 'show', (view) =>
      # Close spinner when result view was shown
      @spinner.close()
      view.on 'sync:collection', =>
        # ... and again when additional model was fetched
        @spinner.close()
      # Show spinner again while loading more cards
      view.on 'more:collection', =>
        @spin()

  spin: ->
    @spinner.show new SpinnerView()

  onShow: ->
    @spin()
