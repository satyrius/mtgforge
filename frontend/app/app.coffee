Backbone = require 'backbone'
require '../vendor/scripts/backbone.meta'
$ = require 'jquery'
require '../vendor/scripts/jquery.unserialize'
Backbone.$ = $
Router = require './router'
require = './helpers'

module.exports = new Router()
