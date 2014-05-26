$ = require 'jquery'
_ = require 'underscore'
Marionette = require 'backbone.marionette'

module.exports = class ResultView extends Marionette.CollectionView
  itemView: require './card'
  emptyView: require './empty'

  initialize: ->
    @body = $ 'body'
    ($ window).on 'scroll.SerpResult', _.throttle(_.bind(@checkScroll, @), 500)

    # Notify related views about collection was synced or started loading more
    @listenTo @collection, 'sync', =>
      @trigger 'collection:sync'
    @listenTo @collection, 'more', =>
      @trigger 'collection:more'

  onClose: ->
    ($ window).off 'scroll.SerpResult'

  checkScroll: ->
    # TODO check scroll direction to handle scroll down only
    return if @collection.isPending() or not @children.length
    # TODO cache last child and update it with collection
    lastCard = @children.findByIndex(@children.length - 1)
    windowBottomPosition = @body.scrollTop() + window.outerHeight
    if windowBottomPosition >= lastCard.$el.offset().top
      @collection.loadMore()
