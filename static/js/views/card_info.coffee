class Forge.CardInfoView extends Backbone.View
    template: window.MEDIA.templates['templates/search/card_info.jst'].render

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

    reset: () ->
        @_rendered = false
        @_lastPosition = null
        @$el.hide()

    render: () =>
        if @card and @cardElement
            # Calculate arrow position and render template
            arrowPosition = @cardElement.offset().left +
                @parent.getCardInfoOffset()
            html = @template({
                card: @card.toJSON(),
                arrowPosition: arrowPosition
            })

            unless @_rendered
                # It is the first time this view rendered, so wa have to
                # replace @el content compelete with rendered html and
                # update @$el reference to the right selector
                @$el = $(@el).replaceWith $(html)
                @delegateEvents()
            else
                # Otherwise we can update inner html and data-id
                @$el.html($(html).html()).data('id', @card.id)

            # Move card info block after card's row if card is from another row
            row = @cardElement.closest('.td-serp-row')
            index = row.siblings('.td-serp-row').andSelf().index(row)
            unless @_rendered and @_lastPosition is index
                row.after(@$el)
                @_lastPosition = index

            # Mark this view as rendered. This means that it has once rendered
            # @el which was attached to DOM tree.
            @_rendered = true

    hide: () ->
        @$el.hide()

    show: () ->
        if @card
            @$el.slideDown 200, () =>
                windowBottom = $('body').scrollTop() + window.outerHeight
                infoBottom =
                    @$el.offsetParent().offset().top + @$el.offset().top +
                    @$el.outerHeight() + @parent.CARD_MARGIN
                offset = windowBottom - infoBottom
                if offset < 0
                    $('body').scrollTop($('body').scrollTop() - offset)


    toggle: (card, cardElement) ->
        if @_rendered and @card.id is card.id and @$el.is(':visible')
            @hide()
        else
            @card = card
            @cardElement = $(cardElement)
            @render()
            @show()

    showPrevious: () ->
        [card, el] = @parent.getPreviousCard(@card)
        if card
            @toggle(card, el)

    showNext: () ->
        [card, el] = @parent.getNextCard(@card)
        if card
            @toggle(card, el)

