class Forge.SidebarView extends Backbone.View
    el: "#sidebar"
    template: window.MEDIA.templates['templates/sidebar.jst'].render
    events:
        "click .filter-toggle" : "handleFilterToggleClick"
        "click .filter-reset" : "resetFilters"
    
    initialize: () ->
        @render()

    subscriptions:
        'search:confirm': 'updateToggles'

    render: () ->
        @$el.html(@template())

    _filterData:
        color: []
        cmc: []
        type: []
        rarity: []

    handleFilterToggleClick: (event) ->
        # INFO: Defer is done to let bootstrap.js toggles do it's work
        # with classes first
        _.defer(@_handleFilterToggleClick, event)
    
    _handleFilterToggleClick: (event) =>
        button  = $(event.target).closest('.filter-toggle')
        data =  button.data('forge-filter-toggle')
        active = button.hasClass('active')
        for key, value of data
            if active
                @_filterData[key].push(value)
            else
                @_filterData[key] = _.without(@_filterData[key], value)
        Backbone.Mediator.publish("search:q", @_filterData)

    updateToggles: (query) ->
        # this is prototype, what you want??
        @_filterData = 
            color: []
            cmc: []
            type: []
            rarity: []
        query = $.unserialize(query)
        delete query.q
        $(".filter-toggle").removeClass("active")
        for key, value of query
            if typeof value == 'string'
                @_filterData[key].push(value) if not _.has(@_filterData[key], value)
                $(".filter-toggle.#{key + '' + value}", @$el).addClass('active')
            else
                for supervalue in value
                    @_filterData[key].push(supervalue) if not _.has(@_filterData[key], supervalue)
                    $(".filter-toggle.#{key + '' + supervalue}", @$el).addClass('active')

    resetFilters: () ->
        @_filterData =
            color: []
            cmc: []
            type: []
            rarity: []
        Backbone.Mediator.publish("search:q", @_filterData)
