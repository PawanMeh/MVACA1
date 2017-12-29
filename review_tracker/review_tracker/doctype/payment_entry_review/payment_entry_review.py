# -*- coding: utf-8 -*-
# Copyright (c) 2017, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import utils,_,msgprint

class PaymentEntryReview(Document):
	def validate(self):
		if self.payment_entry:
			payment_entry_check = frappe.db.sql("""select name from `tabPayment Entry Review` 
			where payment_entry = %s""",(self.payment_entry))
			if payment_entry_check:
				name = payment_entry_check[0][0]
				if self.name == name:
					pass
				else:
					frappe.throw(_("Duplicate Payment Entry already exists on : {0}").format(name))

		if self.get("__islocal") == 1:
			table = "review_checklist"
			rev_question_detail = list(frappe.db.sql("""select question
								from `tabReview Question Detail`
								where parent = %s""","Payment Entry",as_dict=1))
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
									where parent = %s""","Payment Entry",as_dict=1))
				self.set(table, [])
				for d in rev_question_detail:
					self.append(table, d)
				for d in self.review_checklist:
					d.review = "No"

		name_check = frappe.db.sql("""select name from `tabPayment Entry Review` where name = %s""",(self.name))
		if name_check:
			pass
		else:
			self.per_date = frappe.utils.nowdate()

	def before_save(self):
		self.per_date = frappe.utils.nowdate()
		if self.docstatus == 0:
			frappe.db.sql("""update `tabPayment Entry` 
							set per_status = "Initiated" 
							where name = %s""",self.payment_entry)

	def on_submit(self):
		self.per_date = frappe.utils.nowdate()
		frappe.db.sql("""update `tabPayment Entry Review` 
						set per_status = "Done" 
						where name = %s""",self.name)
		for d in self.review_checklist:
			if d and (d.review == "No" or not d.review):
				frappe.throw(_("Review checklist should be set to 'Yes' or 'NA' before submitting"))
		doc = frappe.get_doc("Payment Entry",self.payment_entry)
		doc.per_status = "Done"
		doc.save()