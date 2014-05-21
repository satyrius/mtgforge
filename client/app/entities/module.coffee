Marionette = require 'backbone.marionette'

CardSet = require './models/card_set'
CardSetsCollection = require './collections/card_sets'

Card = require './models/card'
CardsCollection = require './collections/cards'

cache = {}

API =
  getCardSets: ->
    cache.cardSets = new CardSetsCollection() unless cache.cardSets
    return cache.cardSets

  getCardSet: (data) ->
    new CardSet data

  getCardsBySet: (cardSet) ->
    new CardsCollection [], set: cardSet

  getCardsByFTS: (query) ->
    new CardsCollection [], fts: query

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      API.getCardSets()

    @app.reqres.setHandler 'cardset:entity', (data) ->
      API.getCardSet data

    @app.reqres.setHandler 'card:entities:by_set', (cardSet) ->
      API.getCardsBySet cardSet

    @app.reqres.setHandler 'card:entities:fts', (query) ->
      API.getCardsByFTS query
