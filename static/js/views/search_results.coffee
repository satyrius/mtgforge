class Forge.SearchResultsView extends Backbone.View
    el: '#td-main'
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
        'click .td-card': 'showCardInfo'

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
        
        $("#td-search-results", @$el).append(html)

    checkScroll: () =>
        return if @loading
        lastCard = $('.td-card', @$el).last()
        return if lastCard.length == 0
        lastCardTop = lastCard.find('img').offset().top
        windowBottomPosition = $("body").scrollTop() + window.outerHeight
        if windowBottomPosition >= lastCardTop and @data.meta.total_count > @data.meta.offset + @data.meta.limit
            @data.loadNext()
            @loading = true
    
    checkRows: () =>
        return if @initialCardsInRow == @cardsInRow()
        $("#td-search-results", @$el).height($("#td-search-results", @$el).height())
        $("#td-search-results", @$el).empty()
        @addCards(@data.toJSON())
        $("#td-search-results", @$el).height('auto')
        @initialCardsInRow = @cardsInRow()


    cardsInRow: () ->
        Math.floor($('#td-search-results', @$el).width()/(@CARD_WIDTH + @CARD_MARGIN))
    
    showCardInfo: (event) =>
        $('#td-card-info', @$el).remove()
        row = $(event.target).closest('.td-serp-row')
        card = @data.get($(event.target).data('id'))
        row.after(@cardInfoTemplate({card: card.toJSON()}))
        $('#td-card-info', @$el).slideDown(300)

