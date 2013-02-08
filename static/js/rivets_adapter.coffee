rivets.configure({
    adapter: {
        subscribe: (obj, keypath, callback) ->
            obj.on('change:' + keypath, callback)
        unsubscribe: (obj, keypath, callback) ->
            obj.off('change:' + keypath, callback)
        read: (obj, keypath) ->
            return obj.get(keypath)
        publish: (obj, keypath, value) ->
            obj.set(keypath, value)
    }
})
