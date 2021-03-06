# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils,_,msgprint

class PurchaseInvoiceReview(Document):
	def validate(self):
		if self.purchase_invoice:
			pur_invoice_check = frappe.db.sql("""select name from `tabPurchase Invoice Review` 
			where purchase_invoice = %s""",(self.purchase_invoice))
			if pur_invoice_check:
				name = pur_invoice_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Duplicate Purchase Inovice already exists on : {0}").format(name))

		if self.get("__islocal") == 1 and not self.review_checklist:
			table = "review_checklist"
			rev_question_detail = list(frappe.db.sql("""select question
								from `tabReview Question Detail`
								where parent = %s""","Purchase Invoice",as_dict=1))
			self.set(table, [])
			for d in rev_question_detail:
				self.append(table, d)
			for d in self.review_checklist:
				d.review = "No"
		else:
			if self.review_checklist:
				pass
			else:
				table = "review_checklist"
				rev_question_detail = list(frappe.db.sql("""select question
									from `tabReview Question Detail`
									where parent = %s""","Purchase Invoice",as_dict=1))
				self.set(table, [])
				for d in rev_question_detail:
					self.append(table, d)
				for d in self.review_checklist:
					d.review = "No"

		name_check = frappe.db.sql("""select name from `tabPurchase Invoice Review` where name = %s""",(self.name))
		if name_check:
			pass
		else:
			self.pir_date = frappe.utils.nowdate()

	def before_save(self):
		for d in self.review_checklist:
			if d and (d.review == "No"):
				frappe.throw(_("Review checklist should be set to 'Yes', 'NA' or 'Not Sure' before saving"))
		self.pir_date = frappe.utils.nowdate()
		if self.docstatus == 0:
			frappe.db.sql("""update `tabPurchase Invoice` 
							set pir_status = "Initiated", pir = %s
							where name = %s""",(self.name,self.purchase_invoice))

	def on_submit(self):
		self.pir_date = frappe.utils.nowdate()
		frappe.db.sql("""update `tabPurchase Invoice Review` 
						set pir_status = "Done" 
						where name = %s""",self.name)
		for d in self.review_checklist:
			if d and (d.review == "No" or d.review == "Not Sure" or not d.review):
				frappe.throw(_("Review checklist should be set to 'Yes' or 'NA' before submitting"))
		doc = frappe.get_doc("Purchase Invoice",self.purchase_invoice)
		doc.pir_status = "Done"
		doc.save()
