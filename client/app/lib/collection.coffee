Backbone = require 'backbone'
_ = require 'underscore'
resolveUrl = require './url'

module.exports = class ApiCollection extends Backbone.Collection
  url: ->
    resolveUrl _.result(@, '_url')
