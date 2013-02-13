class Forge.SearchResultsView extends Backbone.View
    el: '#main'
    template: window.MEDIA.templates['templates/search/results.jst'].render
    newCardsTemplate: window.MEDIA.templates['templates/search/new_card.jst'].render

    loading: false
    subscriptions:
        'cards:fetched': 'render'
        'cardsCollection:updated': 'addCards'

    render: (data) ->
        @data = data
        @$el.html(@template({cards: data}))
        $(document).on('scroll', @checkScroll)

    addCards: (data) ->
        @loading = false
        $("ul", @$el).append(@newCardsTemplate({cards: data}))

    checkScroll: () =>
        return if @loading
        lastCardTop = $(".card", @$el).last().find('img').offset().top
        windowBottomPosition = $("body").scrollTop() + window.outerHeight

        if windowBottomPosition >= lastCardTop and @data.meta.total_count > @data.meta.offset + @data.meta.limit
            @data.loadNext()
            @loading = true

