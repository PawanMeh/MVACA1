from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cstr
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

@frappe.whitelist()
def make_pi_review(docname):
	pi = frappe.get_doc("Purchase Invoice", docname)
	pir = frappe.new_doc("Purchase Invoice Review")
	pir.purchase_invoice = pi.name
	pir.posting_date = pi.posting_date
	pir.review = "No"
	table = "review_checklist"
	rev_question_detail = list(frappe.db.sql("""select question
						from `tabReview Question Detail`
						where parent = %s""","Purchase Invoice",as_dict=1))
	pir.set(table, [])
	for d in rev_question_detail:
		pir.append(table, d)
	return pir.as_dict()

@frappe.whitelist()
def make_si_review(docname):
	si = frappe.get_doc("Sales Invoice", docname)
	sir = frappe.new_doc("Sales Invoice Review")
	sir.sales_invoice = si.name
	sir.posting_date = si.posting_date
	sir.review = "No"
	table = "review_checklist"
	rev_question_detail = list(frappe.db.sql("""select question
						from `tabReview Question Detail`
						where parent = %s""","Sales Invoice",as_dict=1))
	sir.set(table, [])
	for d in rev_question_detail:
		sir.append(table, d)
	return sir.as_dict()

@frappe.whitelist()
def make_je_review(docname):
	je = frappe.get_doc("Journal Entry", docname)
	jer = frappe.new_doc("Journal Entry Review")
	jer.journal_entry = je.name
	jer.posting_date = je.posting_date
	jer.review = "No"
	table = "review_checklist"
	rev_question_detail = list(frappe.db.sql("""select question
						from `tabReview Question Detail`
						where parent = %s""","Journal Entry",as_dict=1))
	jer.set(table, [])
	for d in rev_question_detail:
		jer.append(table, d)
	return jer.as_dict()

@frappe.whitelist()
def make_pe_review(docname):
	pe = frappe.get_doc("Payment Entry", docname)
	per = frappe.new_doc("Payment Entry Review")
	per.payment_entry = pe.name
	per.posting_date = pe.posting_date
	per.review = "No"
	table = "review_checklist"
	rev_question_detail = list(frappe.db.sql("""select question
						from `tabReview Question Detail`
						where parent = %s""","Payment Entry",as_dict=1))
	per.set(table, [])
	for d in rev_question_detail:
		per.append(table, d)
	return per.as_dict()