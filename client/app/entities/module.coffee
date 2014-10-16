$ = require 'jquery'
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

  loadMoreCards: (collection) ->
    # Use last searched cards collection if nothing specified explicitly
    collection = cache.cards unless collection
    collection.loadMore() if collection

  _resolvedDefer: ->
    # This deferred stub used to handle `return null` cases in the same manner
    # as if actual data will be returned
    return (new $.Deferred).resolve()

  getCard: (id) ->
    deferred = new $.Deferred
    # Check latest collection for the needle
    card = cache.cards.get id if cache.cards
    return (deferred.resolve card) if card
    card = new Card id: id
    card.fetch().done ->
      deferred.resolve card
    return deferred

  getNextCard: (currentCard) ->
    idx = if cache.cards then cache.cards.indexOf currentCard else -1
    return @_resolvedDefer() if idx < 0
    return cache.cards.deferredAt (idx + 1)

  getPrevCard: (currentCard) ->
    idx = if cache.cards then cache.cards.indexOf currentCard else -1
    return @_resolvedDefer() unless idx > 0
    return cache.cards.deferredAt (idx - 1)

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      API.getCardSets()

    @app.reqres.setHandler 'cardset:entity', (data) ->
      API.getCardSet data

    @app.reqres.setHandler 'card:entities', (query) ->
      API.getCards query

    @app.commands.setHandler 'more:card:entities', (collection) ->
      API.loadMoreCards collection

    @app.reqres.setHandler 'card:entity', (id) ->
      API.getCard id

    @app.reqres.setHandler 'next:card:entity', (currentCard) ->
      API.getNextCard currentCard

    @app.reqres.setHandler 'prev:card:entity', (currentCard) ->
      API.getPrevCard currentCard
