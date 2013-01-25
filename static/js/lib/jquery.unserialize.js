(function($){
	$.unserialize = function(serializedString){
		var str = decodeURI(serializedString);
        if (str.charAt(0) == "?") {
            str = str.slice(1);
        }
		var pairs = str.split('&');
        
		var obj = {};
        for (var p in pairs) {
            var splitted = pairs[p].split("=");
            obj[splitted[0]] = splitted[1];
        }
		return obj;
	};
})(jQuery);
