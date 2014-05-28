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
      oldUrl = @url
      @url = @meta.next
      @deferred = @fetch update: true, remove: false
      @deferred.done =>
        @url = oldUrl
