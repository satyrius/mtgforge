Backbone = require 'backbone'
path = require 'path'
conf = require '../config'

module.exports = class ApiModel extends Backbone.Model
  url: ->
    url = super()
    path.join(conf.apiBaseUrl, url)
