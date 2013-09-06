class Forge.IndexView extends Backbone.View
    el: "#td-main"
    template: window.MEDIA.templates['templates/index.jst'].render
    events:
        "click .card-set" : "handleCardSetClick"

    render: () ->
        @$el.html(@template())
