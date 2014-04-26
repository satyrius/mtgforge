Backbone = require 'backbone'
require '../vendor/scripts/backbone-mediator'
$ = require 'jquery'
_ = require 'underscore'
IndexView = require './views/index'
SearchView = require './views/search'
SearchResultsView = require './views/search_results'
SpinnerView = require './views/spinner'
CardsCollection = require './collections/cards'

module.exports = class Router extends Backbone.Router
  constructor: (options) ->
    super(options)
    @searchView = new SearchView({app: @})
    Backbone.Mediator.subscribe 'search:q', (query) =>
      query = $.unserialize query if typeof query == 'string'
      q = _.extend @query, query
      @navigate "search?#{$.serialize(q, true)}", {trigger: true}

  query: {}

  routes:
    '': 'index'
    'search?:params' : 'search'

  index: ->
    unless @indexView?
      @indexView = new IndexView({app: @})
    @indexView.render()

  search: (query) ->
    query = query
    unless @searchResultsView?
      @searchResultsView = new SearchResultsView({app: @})

    unless @spinnerView?
      @spinnerView = new SpinnerView({app: @})

    unless @cardsCollection?
      @cardsCollection = new CardsCollection({app: @})

    Backbone.Mediator.publish 'cards:loading'
    @cardsCollection.fetch({
      data: query
    }).done =>
      Backbone.Mediator.publish 'cards:fetched', @cardsCollection
    Backbone.Mediator.publish 'search:confirm', query
