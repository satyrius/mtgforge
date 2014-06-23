BaseModule = require '../base'
ModalRegion = require './regions/modal'

module.exports = class SerpModule extends BaseModule
  Controller: require './controller'
  Router: require './router'

  initialize: (options) ->
    super options

    @app.commands.setHandler 'cards:search', (query, navigate) =>
      if navigate
        @app.execute 'search:navigate', query
      @controller.listCards query

    @app.addRegions
      modal:
        selector: '#td-modal'
        regionType: ModalRegion
