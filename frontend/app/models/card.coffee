Backbone = require 'backbone'

module.exports = class Card extends Backbone.Model
    url: "api/v1/cards/"
