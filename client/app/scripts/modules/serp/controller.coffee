ApplicationController = require '../../controller'

module.exports = class SerpController extends ApplicationController
  mainView: require './views/main'

  listCards: ->
    @show new @mainView
