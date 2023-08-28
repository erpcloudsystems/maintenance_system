# -*- coding: utf-8 -*-
# Copyright (c) 2020, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MaintenancePayment(Document):
# Cancel All GL Entry Linked With Given Condition
	def on_cancel(self):
		gl = frappe.get_list('GL Entry', filters={'voucher_no': self.name}, fields=['name'])
		for i in gl:
			gl_entry = frappe.get_doc("GL Entry",i)
			gl_entry.cancel()
			gl_entry.delete()

		for d in self.references:
			morder, mproc, type, mdir = frappe.db.get_value("Maintenance Invoice", d.reference_name ,["maintenance_order","processing","processing_type","maintenance_directing"])
			mi = frappe.get_doc("Maintenance Invoice",d.reference_name)
			mi.outstanding_amount += d.allocated_amount
			if mi.outstanding_amount == 0:
				mi.status = "Paid"
				mi.save(ignore_permissions=True)

			if mi.outstanding_amount != 0:
				mi.status = "Unpaid"
				mi.save(ignore_permissions=True)

				if morder:
					mo = frappe.get_doc("Maintenance Order",morder)
					mo.status = "Unpaid"
					mo.flags.ignore_mandatory=True
					mo.save(ignore_permissions=True)

				if mproc:
					mp = frappe.get_doc(type,mproc)
					mp.status = "Unpaid"
					mp.save(ignore_permissions=True)

				if mdir:
					mo = frappe.get_doc("Maintenance Directing",mdir)
					mo.status = "Unpaid"
					mo.flags.ignore_mandatory=True
					mo.save(ignore_permissions=True)


			mi = frappe.get_list('GL Entry', filters={'voucher_no': self.name,"against_voucher":d.reference_name}, fields=['name'])
			for i in mi:
				gl_entry = frappe.get_doc("GL Entry",i)
				gl_entry.cancel()
				gl_entry.delete()

	def on_submit(self):
		if self.unallocated_amount > 0:
			self.status = "Balance Available"
			self.save()

		if self.unallocated_amount == 0:
			self.status = "Allocated"
			self.save()

		if not self.references:
			gl_entry = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"party_type": "Customer",
			"party": self.party,
			"against" : self.paid_to,
			"cost_center": self.cost_center,
			"account": self.paid_from,
			"unallocated": 1,
			"credit": self.unallocated_amount,
			"credit_in_account_currency": self.unallocated_amount,
			"remarks": "Amount {} {} From {}".format(self.paid_amount, self.payment_type, self.party)
			})
			gl_entry.insert(ignore_permissions=True)
			gl_entry.submit()

		if self.references:
			for d in self.references:
				gl_entry = frappe.get_doc({
				"doctype": "GL Entry",
				"posting_date": self.posting_date,
				"against_voucher_type": d.reference_doctype,
				"against_voucher": d.reference_name,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				"party_type": "Customer",
				"party": self.party,
				"against" : self.paid_to,
				"cost_center": self.cost_center,
				"account": self.paid_from,
				"credit": d.allocated_amount,
				"credit_in_account_currency": d.allocated_amount,
				"remarks": "Amount {} {} From {}, Amount {} Against {} {}".format(self.paid_amount, self.payment_type, self.party,d.allocated_amount,d.reference_doctype,d.reference_name)
				})
				gl_entry.insert(ignore_permissions=True)
				gl_entry.submit()

				if d.reference_doctype == "Maintenance Invoice":
					mi = frappe.get_doc("Maintenance Invoice",d.reference_name)
					morder, mproc, type, mdir = frappe.db.get_value("Maintenance Invoice", d.reference_name ,["maintenance_order","processing","processing_type","maintenance_directing"])
					mi.outstanding_amount = d.pending
					if d.pending == 0:
						mi.status = "Paid"
						mi.save(ignore_permissions=True)
						if morder:
							mo = frappe.get_doc("Maintenance Order",morder)
							mo.status = "Paid"
							mo.flags.ignore_mandatory=True
							mo.save(ignore_permissions=True)

						if mproc:
							mp = frappe.get_doc(type,mproc)
							mp.status = "Paid"
							mp.save(ignore_permissions=True)

						if mdir:
							mo = frappe.get_doc("Maintenance Directing",mdir)
							mo.status = "Paid"
							mo.flags.ignore_mandatory=True
							mo.save(ignore_permissions=True)

					else:
						mi.save(ignore_permissions=True)



			if self.unallocated_amount > 0:
				gl_entry = frappe.get_doc({
				"doctype": "GL Entry",
				"posting_date": self.posting_date,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				"party_type": "Customer",
				"party": self.party,
				"against" : self.paid_to,
				"cost_center": self.cost_center,
				"account": self.paid_from,
				"unallocated": 1,
				"credit": self.unallocated_amount,
				"credit_in_account_currency": self.unallocated_amount,
				"remarks": "Amount {} {} From {}, Amount {} Against {} {}".format(self.paid_amount, self.payment_type,self.party,d.allocated_amount,d.reference_doctype,d.reference_name)
				})
				gl_entry.insert(ignore_permissions=True)
				gl_entry.submit()



		gl = frappe.get_doc({
		"doctype": "GL Entry",
		"posting_date": self.posting_date,
		"voucher_type": self.doctype,
		"voucher_no": self.name,
		"cost_center": self.cost_center,
		"account": self.paid_to,
		"against" : self.party,
		"debit": self.paid_amount,
		"debit_in_account_currency": self.paid_amount,
		"remarks": "Amount {} {} From {}".format(self.paid_amount, self.payment_type, self.party)
		})
		gl.insert(ignore_permissions=True)
		gl.submit()



@frappe.whitelist(allow_guest=True)
def getMINV(party):
	pe = frappe.db.sql("""select name,posting_date,rounded_total,outstanding_amount from `tabMaintenance Invoice` where
                        outstanding_amount > 0 and docstatus = 1 and customer = %s;""",(party),as_list=1)
	return pe if pe else ""

