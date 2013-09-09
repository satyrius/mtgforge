class Forge.CardSet extends Backbone.Model
    initialize: () ->
        @set "year", (@get "released_at")[..3]
        @queryFilter = {set: @get "acronym"}

    getSearchUrl: () ->
        unless @_searchUrl?
            @_searchUrl = "search?#{$.serialize(@queryFilter, true)}"
        return @_searchUrl
