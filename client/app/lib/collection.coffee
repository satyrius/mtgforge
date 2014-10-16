Backbone = require 'backbone'
_ = require 'underscore'
urls = require './urls'

module.exports = class ApiCollection extends Backbone.Collection
  url: ->
    @resolveApiUrl _.result(@, '_url')

  resolveApiUrl: (uri) ->
    urls.resolveApiUrl uri.replace(/\/?$/, '/')
