# Copyright (c) 2013, hello@openetech.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt,cstr

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_file_data(filters)
	return columns, data
	
def get_columns():
	columns = [
		{	"label": _("Company"),
			"fieldname": "company",
			"width": 250,
			"fieldtype": "Link",
			"options": "Company"
		}
		,{
			"label": _("Voucher Type"),
			"fieldname": "voucher_type",
			"width": 120
		},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180
		},
		{
			"label": _("Posting Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Attachments Exists"),
			"fieldname": "attach_exists",
			"fieldtype": "Data",
			"width": 10
		},
		{
			"label": _("No of Attachments"),
			"fieldname": "no_attachments",
			"fieldtype": "Int",
			"width": 150
		}
	]
	return columns

def get_file_data(filters):
	conditions=""
	if filters.from_date:
		conditions += " and date(posting_date) >= %(from_date)s"
	if filters.to_date:
		conditions += " and date(posting_date) <= %(to_date)s"

	data = frappe.db.sql("""select company as "company", 'Sales Invoice' as "voucher_type",
									name as "voucher_no", posting_date as "date"
							from `tabSales Invoice`
							where docstatus in ('1','2') {conditions}
							union
							select company as "company", 'Purchase Invoice' as "voucher_type",
									name as "voucher_no", posting_date as "date"
							from `tabPurchase Invoice`
							where docstatus in ('1','2') {conditions}
							union
							select company as "company", 'Payment Entry' as "voucher_type",
									name as "voucher_no", posting_date as "date"
							from `tabPayment Entry`
							where docstatus in ('1','2') {conditions}
							union
							select company as "company", 'Journal Entry' as "voucher_type",
									name as "voucher_no", posting_date as "date"
							from `tabJournal Entry`
							where docstatus in ('1','2') {conditions}
							""".format(conditions=conditions), filters, as_dict=1)
	dl=list(data)
	data = []
	for row in dl:
		row["attach_exists"]= get_file_attach_exists(row["voucher_type"], row["voucher_no"])
		row["no_attachments"]= get_file_attach_no(row["voucher_type"], row["voucher_no"])
		data.append(row)
	return data
	
def get_file_attach_exists(voucher_type, voucher_name):
	attachment_exists = frappe.db.sql("""select 'X'
										from `tabFile`
										where attached_to_doctype = %s and attached_to_name = %s
										and file_size > 0""", 
										(voucher_type, voucher_name))
	if attachment_exists:
		return "Yes"
	else:
		return "No"
	
def get_file_attach_no(voucher_type, voucher_name):
	attachment_no = frappe.db.sql("""select count(name) as "Attach Count"
										from `tabFile` 
										where attached_to_doctype = %s and attached_to_name = %s
										and file_size > 0""", 
										(voucher_type, voucher_name))
	return attachment_no[0][0]