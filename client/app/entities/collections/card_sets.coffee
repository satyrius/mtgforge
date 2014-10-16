ApiCollection = require '../../lib/collection'
CardSet = require '../models/card_set'

module.exports = class CardSetsCollection extends ApiCollection
  _url: 'card_sets'
  model: CardSet

  comparator: (cs) ->
    return - new Date(cs.get 'released_at')

  initialize: ->
    @deferred = @fetch()
