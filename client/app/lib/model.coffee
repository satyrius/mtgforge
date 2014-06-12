Backbone = require 'backbone'
resolveUrl = require './url'

module.exports = class ApiModel extends Backbone.Model
  url: ->
    resolveUrl super
