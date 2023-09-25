from odoo import models, fields, api, exceptions
import requests

class AccountInvoiceIntegration(models.Model):
    _name = 'account.invoice.integration'
    _description = 'Invoice Integration'

    invoice_id = fields.Many2one('account.move', string='Invoice', required=True)
    external_system_id = fields.Char(string='External System ID')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('error', 'Error'),
    ], string='Status', default='pending', required=True)
    response_message = fields.Text(string='Response Message')

    @api.model
    def _send_invoice_to_external_system(self, invoice):
        # Implemente aqui a lógica para enviar os dados da fatura para o sistema externo via API REST
        # Certifique-se de que a resposta do sistema externo inclua o status e a mensagem de resposta
        # Substitua o URL, payload e headers conforme a configuração do seu sistema externo

        url = 'https://api.external_system.com/invoice'
        payload = {
            'invoice_id': invoice.id,
            'amount_total': invoice.amount_total,
            # Adicione outros campos da fatura aqui
        }
        headers = {
            'Authorization': 'Bearer YOUR_API_KEY',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            # Atualize o registro no modelo account.invoice.integration com o status e a mensagem de resposta
            integration_data = {
                'external_system_id': response.json().get('external_invoice_id'),
                'status': 'success' if response.status_code == 200 else 'error',
                'response_message': response.text,
            }
            invoice.integration_ids.write(integration_data)
        except requests.exceptions.RequestException as e:
            raise exceptions.UserError(f"Error sending invoice to external system: {str(e)}")

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        result = super(AccountMove, self).action_post()

        for invoice in self:
            if invoice.state == 'posted':
                invoice.integration_ids._send_invoice_to_external_system(invoice)

        return result
