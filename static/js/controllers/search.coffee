class Forge.SearchController extends Batman.Controller
    @set "advancedEnabled", false
    routingKey: "search"
    toggleAdvancedEnabled: () ->
        if @get("advancedEnabled")
            @set("advancedEnabled", false)
        else
            @set("advancedEnabled", true)
        console.log "Advanced set to", @get("advancedEnabled")
