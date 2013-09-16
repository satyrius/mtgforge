class Forge.SearchView extends Backbone.View
    el: "#td-search"
    template: window.MEDIA.templates['templates/search/form.jst'].render

    events:
        'change #td-search-form': 'handleSubmit'
        'submit #td-search-form': 'handleSubmit'
        'click #feedback-btn': 'showUserVoice'

    subscriptions:
        'search:confirm': 'updateForm'
        'search:reset': 'resetForm'

    q: ""

    initialize: () ->
        @render()
        $('#q-input').focus()

    _setInput: (q) ->
        @$el.find('#td-q-input').val(q)

    resetForm: () ->
        @q = ""
        @_setInput @q

    updateForm: (query) ->
        q = $.unserialize(query).q
        if q
            @_setInput q.replace(/\+/g, ' ')

    render: () ->
        @$el.html(@template())
        #@$el.find('#q-input').typeahead({
            #source: (query, callback) ->
                #$.get('/api/v1/complete', {q: query}, callback)
        #})

    handleSubmit: (event) ->
        q = $(event.target).serialize()
        Backbone.Mediator.publish('search:q', q)
        false

    showUserVoice: ()->
        unless @UserVoice?
            @UserVoice = window.UserVoice || []
        @UserVoice.push ['showLightbox', 'classic_widget',
            mode: 'full'
            primary_color: '#cc6d00'
            link_color: '#007dbf'
            default_mode: 'feedback'
            forum_id: 222347
        ]
