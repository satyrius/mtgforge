$ = require 'jquery'
_ = require 'underscore'
Marionette = require 'backbone.marionette'

module.exports = class ResultView extends Marionette.CollectionView
  itemView: require './card'
  emptyView: require './empty'

  initialize: ->
    @body = $ 'body'
    ($ window).on 'scroll.SerpResult', _.throttle(_.bind(@checkScroll, @), 500)

    # TODO find a better way to access app instance
    @app = require '../../../app'

    # Notify related views about collection was synced or started loading more
    @listenTo @collection, 'sync', =>
      @trigger 'sync:collection'
    @listenTo @collection, 'more', =>
      @trigger 'more:collection'

    @app.vent.on 'show:card', @scrollTo

  scrollTo: (model) =>
    return unless model and @children.length
    idx = @collection.indexOf model
    return if idx < 0
    view = @children.findByIndex idx
    return unless view
    @body.scrollTop (view.$el.offset().top - @body.offset().top)

  onClose: ->
    ($ window).off 'scroll.SerpResult'

  checkScroll: ->
    # TODO check scroll direction to handle scroll down only
    return if @collection.isPending() or not @children.length
    # TODO cache last child and update it with collection
    lastCard = @children.findByIndex (@children.length - 1)
    windowBottomPosition = @body.scrollTop() + window.outerHeight
    if windowBottomPosition >= lastCard.$el.offset().top
      @app.execute 'more:card:entities'
