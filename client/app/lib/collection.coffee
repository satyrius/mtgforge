Backbone = require 'backbone'
_ = require 'underscore'
path = require 'path'
conf = require '../config'

module.exports = class ApiCollection extends Backbone.Collection
  url: ->
    url = _.result(@, '_url')
    path.join(conf.apiBaseUrl, url)
