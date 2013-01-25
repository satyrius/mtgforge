class Forge.SearchView extends Backbone.View
    el: "#search"
    template: window.MEDIA.templates['templates/search/form.jst'].render

    events:
        'submit #search-form': 'handleSubmit'

    subscriptions:
        'search:confirm': 'updateForm'

    initialize: () ->
        @render()

    updateForm: (query) ->
        q = $.unserialize(query).q.replace('+', ' ')
        @$el.find('#q-input').val(q)

    render: () ->
        @$el.html(@template())
        @$el.find('#q-input').typeahead({
            source: ['Jace', 'Chandra', 'Red', 'Green', 'Blue', 'Black', 'White']
        })

    handleSubmit: (event) ->
        q = $(event.target).serialize()
        Backbone.Mediator.publish('search:q', q) 
        false
