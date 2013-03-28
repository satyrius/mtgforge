class Forge.SearchResultsView extends Backbone.View
    el: '#main'
    template: window.MEDIA.templates['templates/search/results.jst'].render
    newRowTemplate: window.MEDIA.templates['templates/search/new_row.jst'].render
    newCardsTemplate: window.MEDIA.templates['templates/search/new_card.jst'].render
    cardInfoTemplate: window.MEDIA.templates['templates/search/card_info.jst'].render
    CARD_WIDTH: 223
    CARD_HEIGHT: 310
    CARD_MARGIN: 15

    subscriptions:
        'cards:fetched': 'render'
        'cardsCollection:updated': 'addCards'

    events:
        'click .card': 'showCardInfo'

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
        html = ""
        for rowCards in d
            html += @newRowTemplate({cards: rowCards})
        
        $("#search-results", @$el).append(html)

    checkScroll: () =>
        return if @loading
        lastCard = $('.card', @$el).last()
        return if lastCard.length == 0
        lastCardTop = lastCard.find('img').offset().top
        windowBottomPosition = $("body").scrollTop() + window.outerHeight
        if windowBottomPosition >= lastCardTop and @data.meta.total_count > @data.meta.offset + @data.meta.limit
            @data.loadNext()
            @loading = true
    
    checkRows: () =>
        return if @initialCardsInRow == @cardsInRow()
        $("#search-results", @$el).height($("#search-results", @$el).height())
        $("#search-results", @$el).empty()
        @addCards(@data.toJSON())
        $("#search-results", @$el).height('auto')
        @initialCardsInRow = @cardsInRow()


    cardsInRow: () ->
        Math.floor($('#search-results', @$el).width()/(@CARD_WIDTH + @CARD_MARGIN))
    
    showCardInfo: (event) =>
        $('#card-info', @$el).remove()
        row = $(event.target).closest('.serp-row')
        card = @data.get($(event.target).data('id'))
        row.after(@cardInfoTemplate({card: card.toJSON()}))
        $('#card-info', @$el).width((@CARD_WIDTH + @CARD_MARGIN) * @cardsInRow() - @CARD_MARGIN - 80)
        $('#card-info', @$el).slideDown(300)

