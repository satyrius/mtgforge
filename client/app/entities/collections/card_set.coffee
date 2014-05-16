Backbone = require 'backbone'
CardSet = require '../models/card_set'

module.exports = class CardSetCollection extends Backbone.Collection
  url: "/api/v1/card_sets/"
  model: CardSet

  comparator: (cs) ->
    return - new Date(cs.get "released_at")

  initialize: ->
    @deferred = @fetch()
