class Forge.SearchResultsView extends Backbone.View
    el: '#td-main'
    template: window.MEDIA.templates['templates/search/results.jst'].render
    newRowTemplate: window.MEDIA.templates['templates/search/new_row.jst'].render
    newCardsTemplate: window.MEDIA.templates['templates/search/new_card.jst'].render
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

    getCardInfoOffset: () ->
        (@CARD_WIDTH/2) + @CARD_MARGIN - @VIEW_MARGIN

    toggleCardInfo: (event) =>
        target = $(event.target)
        card = @data.get(target.data('id'))
        unless @cardInfoView?
            @cardInfoView = new Forge.CardInfoView({parent: @})
        el = target.closest('.td-card')
        Backbone.Mediator.publish('card:details', card, el)

    getCard: (card, offset) ->
        currentIndex = @data.indexOf(card)
        index = currentIndex + offset
        if 0 <= index <= @data.length
            card = @data.at(index)
            el = $(".td-card img[data-id=\"#{card.id}\"]", @$el).parent()
            if el.length
                return [card, el]
        return [null, null]

    getPreviousCard: (card) ->
        @getCard(card, -1)

    getNextCard: (card) ->
        @getCard(card, +1)
