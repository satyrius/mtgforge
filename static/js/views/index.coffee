class Forge.Views.Index extends Backbone.View
    el: "#app-index"
    template: MEDIA.templates["templates/index.jst"]
    initialize: () ->
        @render()
    render: () ->
        @$el.html @template.render(this)
