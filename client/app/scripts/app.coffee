AppView = require './views/AppView'
SearchModule = require './modules/search/SearchModule'

class App extends Backbone.Marionette.Application
  initialize: =>
    console.log 'Initializing app...'

    @addInitializer (options) =>
      (new AppView()).render()

    @addInitializer (options) =>
      @addRegions
        header: '#td-search'
        main: '#td-main'

    @module 'Search', SearchModule

    @reqres.setHandler 'header:region', => @getRegion('header')
    @reqres.setHandler 'default:region', => @getRegion('main')

    @start()

module.exports = new App()
