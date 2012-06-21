class Forge.Card extends Batman.Model
    @persist Batman.LocalStorage
    @encode 'name', 'cmc'
    @resourceName: "cards"
    @storageKey: 'ads'

    name: ''
    cmc: 0
