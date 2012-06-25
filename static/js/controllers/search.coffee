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
        color: new Batman.Set
        type: new Batman.Set
    })

    advancedEnabled: false

    @accessor "serializedQuery", () ->
        query = @get("query").toJSON()
        for key, param of query
            if !param.length
                delete query[key]
        $.param(query)

    toggle: (element, event, context) =>
        typeAndValue = $(event.target).closest("button").attr("id").split("-toggle-")
        type = typeAndValue[0]
        value = typeAndValue[1]
        query = @get "query.#{type}"
        isEnabled = query.has(value)

        if isEnabled
            query.remove(value)
        else
            query.add(value)
