Backbone.Model.prototype.parse = function(resp, xhr) {
	return (resp && 'cards' in resp) ? (resp['cards'][0] || {}) : resp;
};

Backbone.Collection.prototype.parse = function(resp, xhr) {
	return (resp && 'cards' in resp) ? resp['cards'] : resp;
};

Backbone.Model.prototype.fetch =  function(options) {
    options = options ? _.clone(options) : {};
    var model = this;
    var success = options.success;
    options.success = function(resp, status, xhr) {
        if (!model.set(model.parse(resp, xhr), options)) return false;
        if (success) success(model, resp);
        if (typeof resp.meta === "object") model.meta = _.clone(resp.meta);
        console.log("custom fetch mod", _.clone(resp.meta));
    };
    options.error = Backbone.wrapError(options.error, model, options);
    return (this.sync || Backbone.sync).call(this, 'read', this, options);
}

Backbone.Collection.prototype.fetch = function(options) {
    options = options ? _.clone(options) : {};
    if (options.parse === undefined) options.parse = true;
    var collection = this;
    var success = options.success;
    options.success = function(resp, status, xhr) {
        if (typeof resp.meta === "object") {
            collection.meta = _.clone(resp.meta);
            console.log("custom fetch coll", _.clone(resp.meta));
        }
        collection[options.add ? 'add' : 'reset'](collection.parse(resp, xhr), options);
        if (success) success(collection, resp);
    };
    options.error = Backbone.wrapError(options.error, collection, options);
    return (this.sync || Backbone.sync).call(this, 'read', this, options);
}
