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

  getCards: (query) ->
    # Cache last cards collection to get get cards from it
    cache.cards = new CardsCollection [], query: query
    return cache.cards

  getCard: (id) ->
    # Check latest collection for the needle
    card = cache.cards.get id if cache.cards
    unless card
      card = new Card id: id
      card.deferred = card.fetch()
    return card

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      API.getCardSets()

    @app.reqres.setHandler 'cardset:entity', (data) ->
      API.getCardSet data

    @app.reqres.setHandler 'card:entities', (query) ->
      API.getCards query

    @app.reqres.setHandler 'card:entity', (id) ->
      API.getCard id
