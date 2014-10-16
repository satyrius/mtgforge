Backbone = require 'backbone'
urls = require './urls'

module.exports = class ApiModel extends Backbone.Model
  url: ->
    urls.resolveApiUrl super
