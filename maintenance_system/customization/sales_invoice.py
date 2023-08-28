import frappe


@frappe.whitelist()
def create_maintenance_item(invoice):
    if invoice:
        get_invoice=frappe.get_doc("Sales Invoice",invoice)
        if get_invoice.get("items"):
            for item in get_invoice.get("items"):
                warranty_status,warranty_template,maintenance_categorie=frappe.db.get_value("Item",{"item_code":item.item_code},["warranty_status","warranty_template","maintenance_categories"])
                if warranty_status == "Enabled":
                    maintenance_item=frappe.new_doc("Maintenance Item")
                    maintenance_item.customer=get_invoice.get("customer")
                    maintenance_item.item=item.item_code
                    maintenance_item.warranty_status=warranty_status
                    maintenance_item.warranty_template=warranty_template
                    maintenance_item.warranty_start_date=get_invoice.get("posting_date")
                    maintenance_item.sales_invoice=get_invoice.get("name")
                    maintenance_item.maintenance_categories=maintenance_categorie
                    maintenance_item.item_sold_by_us=1
                    maintenance_item.flags.ignore_mandatory=True
                    maintenance_item.save()
                    maintenance_item.submit()
                    frappe.db.set_value("Sales Invoice",get_invoice.get("name"),"warranty_created",1)
                    frappe.msgprint("Maintenance Item Created Successfully")
        return "Maintenance Item Created Successfully"
