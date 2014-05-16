Backbone = require 'backbone'
Marionette = require 'backbone.marionette'
AppView = require './views/main'
Entities = require './entities/module'
SearchModule  = require './modules/search/module'
ProductsModule = require './modules/products/module'
SerpModule = require './modules/serp/module'

class App extends Marionette.Application
  initialize: ->
    @addInitializer (options) ->
      (new AppView()).render()

    @addInitializer (options) ->
      @addRegions
        header: '#td-search'
        main: '#td-main'

    @module 'Entities', Entities
    @module 'Search', SearchModule
    @module 'Products', ProductsModule
    serp = @module 'Serp', SerpModule

    # Define cross module comunication with vent
    serp.addInitializer ->
      @app.on 'cardset:show', (cardSet) =>
        @controller.showCardSet cardSet

    @reqres.setHandler 'header:region', => @getRegion('header')
    @reqres.setHandler 'default:region', => @getRegion('main')

    @start()

  onInitializeAfter: ->
    # define a route for index page
    @Products.router.appRoute '', 'listProducts'
    Backbone.history.start()

module.exports = new App()
