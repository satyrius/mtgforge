window.jQuery = $ = require 'jquery'
Backbone = require 'backbone'
Backbone.$ = $
require '../vendor/scripts/backbone.tastypie'
require '../node_modules/twitter-bootstrap-3.0.0/js/modal'
Marionette = require 'backbone.marionette'

app = require './app'

$ ->
  app.initialize()
