from odoo import models, fields
from odoo import api


class ForeignExchangeRate(models.Model):
    _name = 'account.foreign.exchange.rate'
    _description = 'Foreign Exchange Rate'

    date = fields.Date(string='Date', required=True)
    currency_from_id = fields.Many2one('res.currency', string='From Currency', required=True)
    currency_to_id = fields.Many2one('res.currency', string='To Currency', required=True)
    exchange_rate = fields.Float(string='Exchange Rate', required=True, digits=(12, 6))





class AccountMove(models.Model):
    _inherit = 'account.move'

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('currency_id')
    def _onchange_currency_id(self):
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            # Encontre a taxa de câmbio correspondente
            exchange_rate = self.env['account.foreign.exchange.rate'].search([
                ('currency_from_id', '=', self.currency_id.id),
                ('currency_to_id', '=', self.company_id.currency_id.id),
                ('date', '=', self.date),
            ], limit=1)

            if exchange_rate:
                # Converta os valores do débito e do crédito para a moeda base
                for line in self.line_ids:
                    if line.debit:
                        line.debit = line
