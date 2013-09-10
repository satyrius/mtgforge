class Forge.SearchResultsView extends Backbone.View
    el: '#td-main'
    template: window.MEDIA.templates['templates/search/results.jst'].render
    newRowTemplate: window.MEDIA.templates['templates/search/new_row.jst'].render
    newCardsTemplate: window.MEDIA.templates['templates/search/new_card.jst'].render
    cardInfoTemplate: window.MEDIA.templates['templates/search/card_info.jst'].render
    CARD_WIDTH: 223
    CARD_HEIGHT: 310
    CARD_MARGIN: 15
    VIEW_MARGIN: 60

    subscriptions:
        'cards:fetched': 'render'
        'cardsCollection:updated': 'addCards'

    events:
        'click .td-card': 'toggleCardInfo'

    loading: false
    render: (data) ->
        @data = data
        @$el.html(@template())
        @addCards(data.toJSON())
        @initialCardsInRow = @cardsInRow()
        $(document).on('scroll', _.throttle(@checkScroll, 100))
        $(window).on('resize', _.throttle(@checkRows, 100))

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
            html += @newRowTemplate({cards: rowCards})

        $('#td-search-results', @$el).append(html)

    checkScroll: () =>
        return if @loading
        lastCard = $('.td-card', @$el).last()
        return if lastCard.length == 0
        lastCardTop = lastCard.find('img').offset().top
        windowBottomPosition = $('body').scrollTop() + window.outerHeight
        if windowBottomPosition >= lastCardTop and @data.meta.total_count > @data.meta.offset + @data.meta.limit
            @data.loadNext()
            @loading = true

    checkRows: () =>
        return if @initialCardsInRow == @cardsInRow()
        $('#td-search-results', @$el).height($('#td-search-results', @$el).height())
        $('#td-search-results', @$el).empty()
        @addCards(@data.toJSON())
        $('#td-search-results', @$el).height('auto')
        @initialCardsInRow = @cardsInRow()


    cardsInRow: () ->
        Math.floor($('#td-search-results', @$el).width()/(@CARD_WIDTH + @CARD_MARGIN))

    getCardInfoElement: () ->
        $('#td-card-info', @$el)

    showCardInfoElement: () ->
        el = @getCardInfoElement()
        el.slideDown(300)

    renderCardInfo: (target) =>
        card = @data.get($(target).data('id'))
        arrowPosition = $(target).offset().left + (@CARD_WIDTH/2) + @CARD_MARGIN - @VIEW_MARGIN
        @cardInfoTemplate({
            card: card.toJSON(),
            arrowPosition: arrowPosition})

    toggleCardInfo: (event) =>
        target = $(event.target)
        row = target.closest('.td-serp-row')
        info = @getCardInfoElement()

        unless info.length
            # If card info element is not created yet, render it's content
            # and insert after card's row
            row.after(@renderCardInfo(event.target))
            @showCardInfoElement()
        else
            id = $(target).data('id')
            sameId = info.data('id') is id

            # Hide info if shown (a.k.a toggle) and immediately return
            if sameId and $(':visible', info).length
                info.hide()
                return

            # Update content and id data if new card info requested
            if not sameId
                info.html(
                    $(@renderCardInfo(event.target)).html()
                ).data('id', id)

                # Then check for row index to move card info element after it
                rows = $('.td-serp-row', @$el)
                rowIndex = rows.index(row)
                oldRowIndex = rows.index(info.prev())
                if rowIndex != oldRowIndex
                    info.hide()
                    info.insertAfter(row)

            # Show card info element and fix scroll
            @showCardInfoElement()
            $('body').scrollTop($(event.target).offset().top - 55)
