var Backbone = require('backbone'),
    _ = require('underscore');

Backbone.Model.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? (resp['objects'][0] || {}) : resp;
};

Backbone.Collection.prototype.parse = function(resp, xhr) {
	return (resp && 'objects' in resp) ? resp['objects'] : resp;
};

_.extend(Backbone.Model.prototype, {
    fetch: function(options) {
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
});

_.extend(Backbone.Collection.prototype, {
    fetch: function(options) {
        options = options ? _.clone(options) : {};
        if (options.parse === void 0) options.parse = true;
        var success = options.success;
        var collection = this;
        options.success = function(resp) {
            var method = options.reset ? 'reset' : 'set';
            collection[method](resp, options);
            if (typeof resp.meta === "object") {
                collection.meta = _.clone(resp.meta);
            }
            if (success) success(collection, resp, options);
            collection.trigger('sync', collection, resp, options);
        };
        wrapError(this, options);
        return this.sync('read', this, options);
    }
});

var wrapError = function (model, options) {
    var error = options.error;
    options.error = function(resp) {
        if (error) error(model, resp, options);
        model.trigger('error', model, resp, options);
    };
};
