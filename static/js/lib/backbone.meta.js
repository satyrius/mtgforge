Backbone.Model.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? (resp['objects'][0] || {}) : resp;
};

Backbone.Collection.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? resp['objects'] : resp;
};

Backbone.Model.prototype.fetch = function(options) {
    options = options ? _.clone(options) : {};
    if (options.parse === void 0) options.parse = true;
    var success = options.success;
    options.success = function(model, resp, options) {
        if (!model.set(model.parse(resp, options), options)) return false;
        if (success) success(model, resp, options);
        if (typeof resp.meta === "object") model.meta = _.clone(resp.meta);
    };
    return this.sync('read', this, options);
}

Backbone.Collection.prototype.fetch = function(options) {
    options = options ? _.clone(options) : {};
    if (options.parse === void 0) options.parse = true;
    var success = options.success;
    options.success = function(collection, resp, options) {
        var method = options.update ? 'update' : 'reset';
        collection[method](resp, options);
        if (typeof resp.meta === "object") {
            collection.meta = _.clone(resp.meta);
        }
        if (success) success(collection, resp, options);
    };
    return this.sync('read', this, options);
}
