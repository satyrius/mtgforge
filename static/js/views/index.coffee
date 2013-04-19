class Forge.IndexView extends Backbone.View
    el: "#td-main"
    template: window.MEDIA.templates['templates/index.jst'].render

    render: () ->
        @$el.html(@template())
