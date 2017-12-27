from frappe import _

def get_data():
	return [
		{	"module_name": "review_tracker",
			"label": _("Set Up"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Review Question",
					"label": "Review Question"
				}
			]
		},
		{	"module_name": "review_tracker",
			"label": _("Review Documents"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Purchase Invoice Review",
					"label": "Purchase Invoice Review",
				}
			]
		},
		{	"module_name": "review_tracker",
			"label": _("Review Documents"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Sales Invoice Review",
					"label": "Sales Invoice Review",
				}
			]
		},
		{	"module_name": "review_tracker",
			"label": _("Review Documents"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Journal Entry Review",
					"label": "Journal Entry Review",
				}
			]
		},
		{	"module_name": "review_tracker",
			"label": _("Review Documents"),
			"icon": "icon-star",
			"items": [
				{	"type": "doctype",
					"name": "Payment Entry Review",
					"label": "Payment Entry Review",
				}
			]
		}
]