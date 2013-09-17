class Forge.CardInfoView extends Backbone.View
  template: require '../templates/search/card_info'

  events:
    'click button.close': 'hide'
    'click button.left': 'showPrevious'
    'click button.right': 'showNext'

  subscriptions:
    'card:details': 'toggle'
    'cards:fetched': 'reset'

  initialize: (options) ->
    super()
    @parent = options.parent
    @reset()
    $(document).on 'keydown', (event) =>
      switch event.keyCode
        when 37 then @showPrevious()
        when 39 then @showNext()

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

  hide: ->
    @$el.hide()

  show: ->
    unless @card and @cardElement
      return

    @$el.slideDown 200, =>
      parentOffset = @$el.offsetParent().offset().top
      scroll = $('body').scrollTop()

      # First scroll to show card element top border
      cardTop = $('img', @cardElement).offset().top - parentOffset
      if cardTop < 0
        cardTop = 0
      if cardTop != scroll
        scroll = scroll - (scroll - cardTop)

      # Then check that card info lower border is visible
      elTop = @$el.offset().top
      elBottom = elTop + @$el.outerHeight() +
        @parent.CARD_MARGIN + parentOffset
      windowBottom = scroll + window.outerHeight
      if elBottom > windowBottom
        scroll += elBottom - windowBottom

      # And at the end check card info top border is visible
      barHeight = Forge.app.searchView.$el.outerHeight()
      if elTop - barHeight < scroll
        scroll -= scroll - elTop + barHeight

      $('body').scrollTop scroll

  toggle: (card, cardElement) ->
    if @_rendered and @card.id is card.id and @$el.is(':visible')
      @hide()
    else
      @card = card
      @cardElement = $(cardElement)
      @render()
      @show()

  showPrevious: ->
    [card, el] = @parent.getPreviousCard @card
    if card
      @toggle card, el

  showNext: ->
    [card, el] = @parent.getNextCard @card
    if card
      @toggle card, el
