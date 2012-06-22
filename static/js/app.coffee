#Hardcore pure js RESTful parse fix
`Backbone.Model.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? (resp['objects'][0] || {}) : resp;
};

Backbone.Collection.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? resp['objects'] : resp;
};`

window.Forge =
    Models: {}
    Collections: {}
    Views: {}

$ ->
    Forge.App = new Forge.Views.App()
    Forge.Search = new Forge.Views.Search()
