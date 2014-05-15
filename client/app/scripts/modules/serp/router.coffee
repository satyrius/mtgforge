Marionette = require 'backbone.marionette'

module.exports = class SerpRouter extends Marionette.AppRouter
  appRoutes:
    'search?:params': 'listCards'
