$ = require 'jquery'
Backbone = require 'backbone'
Backbone.$ = $
require '../../vendor/scripts/backbone.tastypie'
Marionette = require 'backbone.marionette'

app = require './app'

$ ->
  app.initialize()
