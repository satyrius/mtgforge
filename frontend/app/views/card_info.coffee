Backbone = require 'backbone'
BaseView = require './base'
$ = require 'jquery'

module.exports = class CardInfoView extends BaseView
  template: require '../templates/search/card_info'

  events:
    'click button.close': 'hide'
    'click button.left': 'showPrevious'
    'click button.right': 'showNext'

  subscriptions:
    'card:details': 'toggle'
    'cards:fetched': 'reset'
    'search:focus': 'hide'

  initialize: (options) ->
    super(options)
    @parent = options.parent
    @reset()
    $(document).on 'keydown', (event) =>
      if @isOpened()
        switch event.keyCode
          when 27 then @hide(); false # esc
          when 37 then @showPrevious(); false # arrow left
          when 38 then @showPreviousRow(); false # arrow up
          when 39 then @showNext(); false # arrow right
          when 40 then @showNextRow(); false # arror down

  reset: ->
    @_rendered = false
    @_lastPosition = null
    @$el.hide()

  render: =>
    unless @card and @cardElement
      return

    # Calculate arrow position and render template
    arrowPosition = @cardElement.offset().left +
      @parent.getCardInfoOffset()
    html = @template
      card: @card.toJSON(),
      arrowPosition: arrowPosition

    # Card info block positiob after card's row if card is from another row
    row = @cardElement.closest '.td-serp-row'
    index = row.siblings('.td-serp-row').addBack().index row

    unless @_rendered
      # It is the first time this view rendered, so wa have to
      # replace @el content compelete with rendered html and
      # update @$el reference to the right selector
      @$el = $(html).insertAfter(row)
      @el = @$el[0]
      @delegateEvents()
    else
      # Otherwise we can update inner html and data-id
      @$el.html($(html).html()).data('id', @card.id)
      unless @_lastPosition is index
        row.after @$el

    @_lastPosition = index

    # Mark this view as rendered. This means that it has once rendered
    # @el which was attached to DOM tree.
    @_rendered = true

  getScrollToCardElement: ->
      scroll = $('body').scrollTop()

      if @cardElement
        cardTop = $('img', @cardElement).offset().top -
          @cardElement.offsetParent().offset().top
        cardTop = 0 if cardTop < 0
        if cardTop != scroll
          scroll = scroll - (scroll - cardTop)

      return scroll

  hide: ->
    @$el.hide()

    if @cardElement
      $('body').scrollTop @getScrollToCardElement()

  show: ->
    unless @card and @cardElement
      return

    @$el.slideDown 200, =>
      parentOffset = @$el.offsetParent().offset().top

      # First scroll to show card element top border
      scroll = @getScrollToCardElement()

      # Then check that card info lower border is visible
      elTop = @$el.offset().top
      elBottom = elTop + @$el.outerHeight() +
        @parent.CARD_MARGIN + parentOffset
      windowBottom = scroll + window.outerHeight
      if elBottom > windowBottom
        scroll += elBottom - windowBottom

      # And at the end check card info top border is visible
      barHeight = @app.searchView.$el.outerHeight()
      if elTop - barHeight < scroll
        scroll -= scroll - elTop + barHeight

      $('body').scrollTop scroll

  isOpened: ->
    @$el.is(':visible')

  toggle: (card, cardElement) ->
    if @_rendered and @card.id is card.id and @isOpened()
      @hide()
    else
      @card = card
      @cardElement = $(cardElement)
      @render()
      @show()

  move: (offset) ->
    [card, el] = @parent.getCard @card, offset
    if card
      @toggle card, el

  showPrevious: ->
    @move -1

  showNext: ->
    @move 1

  showPreviousRow: ->
    @move -@parent.cardsInRow()

  showNextRow: ->
    @move @parent.cardsInRow()
