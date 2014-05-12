AppView = require './views/AppView'
Entities = require './entities/Entities'
SearchModule  = require './modules/search/SearchModule'
ProductsModule = require './modules/products/ProductsModule'
Router = require './router'

class App extends Backbone.Marionette.Application
  initialize: ->
    @addInitializer (options) ->
      (new AppView()).render()

    @addInitializer (options) ->
      @addRegions
        header: '#td-search'
        main: '#td-main'

    @addInitializer (options) ->
      new Router()

    @module 'Entities', Entities
    @module 'Search', SearchModule
    @module 'Products', ProductsModule

    @reqres.setHandler 'header:region', => @getRegion('header')
    @reqres.setHandler 'default:region', => @getRegion('main')

    @start()

  onInitializeAfter: ->
    Backbone.history.start()

module.exports = new App()
