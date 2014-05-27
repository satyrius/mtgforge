Backbone = require 'backbone'

module.exports = class Card extends Backbone.Model
  urlRoot: '/api/v1/cards'
  idAttribute: 'id'
