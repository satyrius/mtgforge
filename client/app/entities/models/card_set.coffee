Backbone = require 'backbone'

module.exports = class CardSet extends Backbone.Model
  initialize: ->
    @year = (new Number @get('released_at')[..3]) if @has 'released_at'
    @queryFilter = set: @get 'acronym'

    CORE_SET_RE = /Magic|Edition|Alpha|Beta|Unlimited|Revised/
    REISSUE_RE = ///
      Archenemy
      | Vault
      | Commander
      | Planechase
      | Masters
      | Portal
      | Starter
      | Battle\sRoyale
      | Beatdown
      | Unhinged
      | Unglued
      | Premium
    ///
    DUEL_DECK_RE = /Duel|vs\./
    @type = switch
      when (not @has 'name') or ((@get 'name').search(REISSUE_RE) != -1) then 'other'
      when (@get 'name').search(CORE_SET_RE) != -1 then 'core'
      when (@get 'name').search(DUEL_DECK_RE) != -1 then 'other'
      else 'block'

  isCoreSet: ->
    @type is 'core'

  isBlockSet: ->
    @type is 'block'

  isDuelDecks: ->
    @type is 'duel'
