from openerp import models, api, fields


class product_currency(models.Model):
    _inherit = 'product.template'
    currency_list = fields.One2many('currency.list', 'currency_id', string='Currency List')


class currency_rate_update_service(models.Model):

    _name = "currency.list"
    listt = []
    currency_id = fields.Many2one()
    currency = fields.Many2one('res.currency', string="Currency")
    price = fields.Char(string="Price")


    def onchange_currency(self, cr, uid, ids, currency, context=None):
            res = {}
            currency_obj = self.pool.get('res.currency')
            temp_list = currency_obj.search(cr, uid, [('id', '=', currency)], context=context)

            for i in temp_list:
                self.listt.append(i)

            if currency:
                res['domain'] = {'currency': [('id', 'not in', self.listt)]}
            return res


class account_invoice_line(models.Model):

    _inherit = "account.invoice"

    @api.multi

    def onchange_update(self,currency_id):


        print ">>>>>>>>>>>>>>>>>>>>", self.invoice_line


        for inv_line in self.invoice_line:
            print "inv_line", inv_line
            for curr_list in inv_line.product_id.currency_list:
                print ">>>>>>>>>>>>>>>>>>>>>>>>>", curr_list.currency
                if currency_id == curr_list.currency.id:

                    print currency_id , 'xxx', curr_list.currency.name, curr_list.price
                    self.pool.get('account.invoice.line').write(self._cr, self._uid, inv_line.id, {'price_unit': curr_list.price}, context=None)

                    print">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<"




















    # _inherit = "account.change.currency"
    #
    #
    # def change_currency(self, cr, uid, ids, context=None):
    #     data = self.browse(cr, uid, ids, context=context)[0]
    #     new_currency = data.currency_id.id
    #     obj_inv = self.pool.get('account.invoice')
    #     obj_inv_line = self.pool.get('account.invoice.line')
    #     invoice = obj_inv.browse(self,context['active_id'])
    #     for line in invoice.invoice_line:
    #           for curr_list in line.product_id.currency_list:
    #                 print ">>>>>>>>>>>>>>>>>>>>>>>>>", curr_list.currency
    #                 if invoice.currency_id == curr_list.currency:
    #                     obj_inv_line.write( cr, uid, [line.id], {'price_unit': curr_list.price})
    #
    #     obj_inv.write(cr, uid, [invoice.id], {'currency_id': new_currency}, context=context)
    #     return {'type': 'ir.actions.act_window_close'}
