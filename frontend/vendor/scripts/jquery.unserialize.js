var $ = require('jquery'),
    _ = require('underscore');

$.unserialize = function(serializedString){
    var str = decodeURI(serializedString);
    if (str.charAt(0) == "?") {
	str = str.slice(1);
    }
    var pairs = str.split('&');

    var obj = {};
    for (var p in pairs) {
	var splitted = pairs[p].split("=");
	var supersplitted = splitted[1].split(",");
	if (supersplitted.length > 1) {
	    obj[splitted[0]] = supersplitted;
	} else {
	    obj[splitted[0]] = splitted[1];
	}
    }
    return obj;
};

$.serialize = function(unserializedObject, notIncludeEmpty) {
    var str = "";
    for (var p in unserializedObject) {
	if (!_.isEmpty(unserializedObject[p])) {
	    str = str + [p, "=", unserializedObject[p], "&"].join("");
	}
    }
    str = str.substr(0, str.length - 1);
    return encodeURI(str);
};
