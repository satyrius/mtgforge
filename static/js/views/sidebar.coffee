class Forge.SidebarView extends Backbone.View
    el: "#td-sidebar"
    template: window.MEDIA.templates['templates/sidebar.jst'].render
    events:
        "click .filter-toggle" : "handleFilterToggleClick"
        "click .filter-reset" : "resetFilters"
        "change .filter-sets" : "handleFilterSetsChange"
    
    initialize: () ->
        @render()

    subscriptions:
        'search:confirm': 'updateToggles'

    render: () ->
        @$el.html(@template())
        $(".filter-sets").chosen({no_results_text: "No results matched"})

    _filterData:
        color: []
        cmc: []
        type: []
        rarity: []
        set: []

    handleFilterToggleClick: (event) ->
        # INFO: Defer is done to let bootstrap.js toggles do it's work
        # with classes first
        _.defer(@_handleFilterToggleClick, event)

    handleFilterSetsChange: (event) ->
        data = $(event.target).val()
        @_filterData.set = data
        Backbone.Mediator.publish("search:q", @_filterData)

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
            set: []
        query = $.unserialize(query)
        delete query.q
        $(".filter-sets").val(query.set)
        $(".filter-sets").trigger("liszt:updated")
        delete query.sets
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
            set: []
        Backbone.Mediator.publish("search:q", @_filterData)
