Backbone = require 'backbone'
Handlebars = require 'hbsfy/runtime'
$ = require 'jquery'

Handlebars.registerHelper 'search_href', (object) ->
  if object instanceof Backbone.Model
    query = object.queryFilter
  else
    query = object
  "#search?#{$.serialize(query, true)}"

Handlebars.registerHelper 'get', (model, attribute) ->
  model.get attribute
