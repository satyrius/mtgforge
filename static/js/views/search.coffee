class Forge.SearchView extends Backbone.View
    el: "#search"
    template: window.MEDIA.templates['templates/search/form.jst'].render

    events:
        'change #search-form': 'handleSubmit'
        'submit #search-form': 'handleSubmit'

    subscriptions:
        'search:confirm': 'updateForm'

    q: ""

    initialize: () ->
        @render()
        $('#q-input').focus()

    updateForm: (query) ->
        q = $.unserialize(query).q
        if q
            q = q.replace(/\+/g, ' ')
            @$el.find('#q-input').val(q)

    render: () ->
        @$el.html(@template())
        @$el.find('#q-input').typeahead({
            source: (query, callback) ->
                $.get('/api/v1/complete', {q: query}, callback)
        })

    handleSubmit: (event) ->
        q = $(event.target).serialize()
        Backbone.Mediator.publish('search:q', q) 
        false
