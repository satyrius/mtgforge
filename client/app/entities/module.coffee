Marionette = require 'backbone.marionette'
CardSetCollection = require './collections/card_set'
CardSet = require './models/card_set'

cache = {}

API =
  getCardSets: ->
    cache.cardSets = new CardSetCollection() unless cache.cardSets
    return cache.cardSets

  getCardSet: (data) ->
    return new CardSet data

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()

    @app.reqres.setHandler 'cardset:entity', (data) ->
      return API.getCardSet data
