Backbone = require 'backbone'
BaseView = require './base'
CardInfoView = require './card_info'
_ = require 'underscore'
$ = require 'jquery'
Handlebars = require 'hbsfy/runtime'

Handlebars.registerPartial 'card', require '../templates/search/card'

module.exports = class SearchResultsView extends BaseView
  el: '#td-main'
  template: require '../templates/search/results'
  notFoundTemplate: require '../templates/search/notfound'
  newRowTemplate: require '../templates/search/new_row'
  newCardsTemplate: require '../templates/search/new_card'
  CARD_WIDTH: 223
  CARD_HEIGHT: 310
  CARD_MARGIN: 15
  VIEW_MARGIN: 60

  subscriptions:
    'cards:loading': 'clear'
    'cards:fetched': 'render'
    'cardsCollection:updated': 'addCards'

  events:
    'click .td-card': 'toggleCardInfo'

  loading: false

  clear: ->
    @$el.html ''

  render: (data) ->
    @data = data
    unless @data.length
      @$el.html @notFoundTemplate()
      return

    @$el.html @template()
    @addCards data.toJSON()
    @initialCardsInRow = @cardsInRow()
    $('body').scrollTop 0
    $(document).on 'scroll', _.throttle(@checkScroll, 100)
    $(window).on 'resize', _.throttle(@checkRows, 100)

  addCards: (data) ->
    @loading = false
    d = []
    _.map(data, (card) ->
      if d.length >0 and d[d.length-1].length < @cardsInRow()
        return d[d.length-1].push(card)
      else
        return d.push([card])
    , this)
    html = ''
    for rowCards in d
      html += @newRowTemplate {cards: rowCards}

    $('#td-search-results', @$el).append html

  checkScroll: =>
    return if @loading
    lastCard = $('.td-card', @$el).last()
    return if lastCard.length == 0
    lastCardTop = lastCard.find('img').offset().top
    windowBottomPosition = $('body').scrollTop() + window.outerHeight
    if windowBottomPosition >= lastCardTop and @data.meta.total_count > @data.meta.offset + @data.meta.limit
      @data.loadNext()
      @loading = true

  checkRows: =>
    return if @initialCardsInRow == @cardsInRow()
    $('#td-search-results', @$el).height($('#td-search-results', @$el).height())
    $('#td-search-results', @$el).empty()
    @addCards @data.toJSON()
    $('#td-search-results', @$el).height 'auto'
    @initialCardsInRow = @cardsInRow()

  cardsInRow: ->
    resultsWidth = $('#td-search-results', @$el).width()
    Math.floor resultsWidth / (@CARD_WIDTH + @CARD_MARGIN)

  getCardInfoOffset: ->
    (@CARD_WIDTH / 2) + @CARD_MARGIN - @VIEW_MARGIN

  toggleCardInfo: (event) =>
    target = $ event.target
    card = @data.get target.data('id')
    unless @cardInfoView?
      @cardInfoView = new CardInfoView {parent: @, app: @app}

    el = target.closest '.td-card'
    Backbone.Mediator.publish 'card:details', card, el

  getCard: (card, offset) ->
    currentIndex = @data.indexOf card
    index = currentIndex + offset
    if 0 <= index <= @data.length
      card = @data.at index
      el = $(".td-card img[data-id=\"#{card.id}\"]", @$el).parent()
      if el.length
        return [card, el]

    return [null, null]
