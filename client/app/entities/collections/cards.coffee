$ = require 'jquery'
ApiCollection = require '../../lib/collection'
Card = require '../models/card'

module.exports = class CardsCollection extends ApiCollection
  _url: 'cards/search'
  model: Card

  initialize: (models, options) ->
    @deferred = @fetch
      data: options.query

  isPending: ->
    @deferred.state() is 'pending'

  loadMore: ->
    if not @isPending() and @meta.next
      @trigger 'more'
      @deferred = @fetch
        url: @resolveApiUrl @meta.next
        update: true,
        remove: false
    return @deferred

  deferredAt: (index) ->
    deferred = new $.Deferred

    model = @at index
    return (deferred.resolve model) if model

    # Load more cards if next card is beyond the last loaded card
    if @models and index >= @models.length and @meta.next
      @loadMore().done =>
        deferred.resolve (@at index)
    else
      deferred.resolve()

    return deferred
