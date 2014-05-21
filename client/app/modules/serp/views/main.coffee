SpinnerView = require './spinner'
Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.Layout
  template: require './templates/main'

  regions:
    info: '#td-serp-info'
    result: '#td-serp-cards'
    spinner: '#td-serp-spinner'

  initialize: ->
    @result.on 'show', (view) =>
      # Close spinner when result view was shown
      @spinner.close()
      view.on 'collection:sync', =>
        # ... and again when additional model was fetched
        @spinner.close()
      # Show spinner again while loading more cards
      view.on 'collection:more', =>
        @spin()

  spin: ->
    @spinner.show new SpinnerView()

  onShow: ->
    @spin()
