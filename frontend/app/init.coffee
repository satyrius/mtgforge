Backbone = require 'backbone'
app = require './app'
$ = require 'jquery'

$ ->
  window.Forge = app
  Backbone.history.start()
