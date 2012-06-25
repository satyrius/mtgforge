class Forge.SearchController extends Batman.Controller
    routingKey: ""
    advancedToggle: (element, event, context) =>
        if @get "advancedEnabled"
            @set "advancedEnabled", false
        else
            @set "advancedEnabled", true
        false

    submitSearch: (element, event, context) ->
        @redirect "/search?#{@get('serializedQuery')}"
        false

    query: Batman({
        q: ""
        color: ""
    })

    advancedEnabled: false

    @accessor "serializedQuery", () ->
        query = @get("query").toJSON()
        for key, param of query
            if !param.length
                delete query[key]
        $.param(query)

    manaToggle: (element, event, context) =>
        color = $(event.target).closest("button").attr("id").replace("mana-toggle-", "")
        queryColor = @get "query.color"
        isEnabled = queryColor.search(color) > -1

        if isEnabled
            @set "query.color", (queryColor.replace(color, ""))
        else
            @set "query.color", (queryColor + color)
    
    #typeToggle: (element, event, context) =>
        #type = $(event.target).closest("button").attr("id").replace("type-toggle-", "")
        #queryType = @get "query.type"
        #isEnabled = queryColor.search(color) > -1

        #if isEnabled
            #@set "query.type", ((queryType+",").replace(color, ""))
        #else
            #@set "query.type", (queryColor + color)
