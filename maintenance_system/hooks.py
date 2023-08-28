# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "maintenance_system"
app_title = "Maintenance System"
app_publisher = "Tech Station"
app_description = "App For maintenance"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "developer@techstation.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/maintenance_system/css/maintenance_system.css"
# app_include_js = "/assets/maintenance_system/js/maintenance_system.js"

# include js, css files in header of web template
# web_include_css = "/assets/maintenance_system/css/maintenance_system.css"
# web_include_js = "/assets/maintenance_system/js/maintenance_system.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

doctype_js = {
    "Sales Order": "public/js/sales_order.js",
    "Delivery Note": "public/js/delivery_note.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    "Item": "public/js/item.js",
    "Customer": "public/js/customer.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "maintenance_system.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "maintenance_system.install.before_install"
# after_install = "maintenance_system.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "maintenance_system.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Maintenance Item": {
        "on_update_after_submit": "maintenance_system.maintenance_system.doctype.maintenance_item.maintenance_item.on_update_data_self"
    },
    "Customer": {
        "validate":"maintenance_system.customization.customer.on_update_mobile"
    },
    # "POS Profile": {
    #     "validate": "maintenance_system.customization.pos_profile.create_delete_pos_profile"
    # }
}


fixtures = [
    {
        "doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
                    "Item-warranty_period-hidden"
                ]
            ]
        ]
    },
    {"dt": "DocType", "filters": [
        ["name", "in", ["Maintenance Schedule List"]]]},
    {"dt": "Client Script", "filters": [
        [
            "dt", "in", [
                "Warranty Template", "Maintenance Item", "Sales Invoice", "Maintenance Schedule List", "Maintenance Team"
            ]
        ]
    ]},

    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Item-warranty_template",
                    "Item-warranty_status",
                    "Item-maintenance_categories",
                    "Sales Order Item-warranty_template",
                    "Sales Order Item-warranty_status",
                    "Delivery Note Item-warranty_template",
                    "Delivery Note Item-warranty_status",
                    "Sales Invoice Item-warranty_template",
                    "Sales Invoice-warranty_created",
                    "Sales Invoice Item-warranty_status",
                    "Payment Entry-allocated_in_maintenance",
                    "Stock Entry-maintenance_products_receipt",
                    "GL Entry-unallocated","Mode of Payment-show_in_maintenance_for_payment",
                    "Customer-mobile","Branch-enable","Branch-default_branch"
                ]
            ]
        ]
    },
    {
        "doctype": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "Maintenance Item","Maintenance User",
                    "Maintenance Directing","Maintenance Invoice",
                    "Maintenance Order",
                    "Maintenance Manager",
                    "Maintenance Internal",
                    "Maintenance External",
                    "Maintenance Payment","Maintenance Commission",
                    "Maintenance Material","Maintenance Supervisor"

                ]
            ]
        ]
    },
    {
        "doctype": "Custom DocPerm",
        "filters": [
            [
                "role",
                "in",
                [
                    "Maintenance Item","Maintenance User",
                    "Maintenance Directing","Maintenance Invoice",
                    "Maintenance Order",
                    "Maintenance Manager",
                    "Maintenance Internal",
                    "Maintenance External",
                    "Maintenance Payment","Maintenance Commission",
                    "Maintenance Material","Maintenance Supervisor"

                ]
            ]
        ]
    },
    {
        "doctype": "Module Profile",
        "filters": [
            [
                "name",
                "in",
                [
                    "Maintenance System"

                ]
            ]
        ]
    },"Workflow","Workflow State"
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"maintenance_system.tasks.all"
# 	],
# 	"daily": [
# 		"maintenance_system.tasks.daily"
# 	],
# 	"hourly": [
# 		"maintenance_system.tasks.hourly"
# 	],
# 	"weekly": [
# 		"maintenance_system.tasks.weekly"
# 	]
# 	"monthly": [
# 		"maintenance_system.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "maintenance_system.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "maintenance_system.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "maintenance_system.task.get_dashboard_data"
# }
