class Forge.SidebarView extends Backbone.View
    el: "#sidebar"
    template: window.MEDIA.templates['templates/sidebar.jst'].render
    
    initialize: () ->
        @render()

    render: () ->
        @$el.html(@template())
