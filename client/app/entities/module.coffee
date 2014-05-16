Marionette = require 'backbone.marionette'
CardSetCollection = require './collections/card_set'

cache = {}

API =
  getCardSets: ->
    cache.cardSets = new CardSetCollection() unless cache.cardSets
    return cache.cardSets

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()
