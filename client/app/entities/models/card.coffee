ApiModel = require '../../lib/model'

module.exports = class Card extends ApiModel
  urlRoot: 'cards'
  idAttribute: 'id'
