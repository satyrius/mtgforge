class Forge.SearchView extends Backbone.View
    el: "#search"
    template: window.MEDIA.templates['templates/search/form.jst'].render

    events:
        'submit #search-form': 'handleSubmit'

    subscriptions:
        'search:confirm': 'updateForm'

    q: ""

    initialize: () ->
        @render()
        $('#q-input').focus()

    updateForm: (query) ->
        q = $.unserialize(query).q.replace(/\+/g, ' ')
        @$el.find('#q-input').val(q)

    render: () ->
        @$el.html(@template())
        @$el.find('#q-input').typeahead({
            source: (query, callback) ->
                $.get('/api/v1/complete', {q: query}, (data) ->
                    arr = []
                    for obj in data.objects
                        arr.push(obj.name)
                    callback(arr)
                )
        })

    handleSubmit: (event) ->
        q = $(event.target).serialize()
        Backbone.Mediator.publish('search:q', q) 
        false
