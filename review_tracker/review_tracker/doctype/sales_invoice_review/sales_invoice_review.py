# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils,_,msgprint

class SalesInvoiceReview(Document):
	def validate(self):
		if self.sales_invoice:
			sales_invoice_check = frappe.db.sql("""select name from `tabSales Invoice Review` 
			where sales_invoice = %s""",(self.sales_invoice))
			if sales_invoice_check:
				name = sales_invoice_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Duplicate Sales Inovice already exists on : {0}").format(name))

		if self.get("__islocal") == 1 and not self.review_checklist:
			table = "review_checklist"
			rev_question_detail = list(frappe.db.sql("""select question
								from `tabReview Question Detail`
								where parent = %s""","Sales Invoice",as_dict=1))
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
									where parent = %s""","Sales Invoice",as_dict=1))
				self.set(table, [])
				for d in rev_question_detail:
					self.append(table, d)
				for d in self.review_checklist:
					d.review = "No"

		name_check = frappe.db.sql("""select name from `tabSales Invoice Review` where name = %s""",(self.name))
		if name_check:
			pass
		else:
			self.sir_date = frappe.utils.nowdate()

	def before_save(self):
		for d in self.review_checklist:
			if d and (d.review == "No"):
				frappe.throw(_("Review checklist should be set to 'Yes', 'NA' or 'Not Sure' before saving"))
		self.sir_date = frappe.utils.nowdate()
		if self.docstatus == 0:
			frappe.db.sql("""update `tabSales Invoice` 
							set sir_status = "Initiated",sir = %s 
							where name = %s""",(self.name,self.sales_invoice))

	def on_submit(self):
		self.sir_date = frappe.utils.nowdate()
		frappe.db.sql("""update `tabSales Invoice Review` 
						set sir_status = "Done" 
						where name = %s""",self.name)
		for d in self.review_checklist:
			if d and (d.review == "No" or d.review == "Not Sure" or not d.review):
				frappe.throw(_("Review checklist should be set to 'Yes' or 'NA' before submitting"))
		doc = frappe.get_doc("Sales Invoice",self.sales_invoice)
		doc.sir_status = "Done"
		doc.save()
