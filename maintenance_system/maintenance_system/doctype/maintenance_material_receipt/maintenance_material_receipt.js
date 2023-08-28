// Copyright (c) 2020, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Material Receipt', {
    // refresh: function(frm) {

    // }
});

frappe.ui.form.on('Maintenance Material Receipt', {
    refresh: function (frm) {
        if (frm.doc.docstatus == 1 && frm.doc.status == "Delivered") {
            frm.add_custom_button(__("Go To Processing"), function () {
                frappe.set_route("Form", frm.doc.processing_type, frm.doc.processing);
            })
        }
    }
});



frappe.ui.form.on("Maintenance Material Receipt", "customer", function (frm) {
    cur_frm.set_query("maintenance_processing", function () {
        return {
            "filters": {
                "customer": frm.doc.customer,
                "status": "Start"
            }
        };
    });
});

frappe.ui.form.on("Maintenance Material Receipt", "onload", function (frm) {
    cur_frm.set_query("maintenance_processing", function () {
        return {
            "filters": {
                "customer": frm.doc.customer,
                "status": "Start"
            }
        };
    });
});

frappe.ui.form.on("Maintenance Material Receipt", "onload", function (frm) {
    // cur_frm.set_query("warehouse", function () {
    //     return {
    //         "filters": {
    //             "is_group": 0
    //         }
    //     };
    // });
});

/*frappe.ui.form.on("Maintenance Material Receipt", "maintenance_processing", function(frm) {
      if (frm.doc.maintenance_processing){
            frappe.model.with_doc("Maintenance Processing", frm.doc.maintenance_processing, function() {
            cur_frm.clear_table("items");
            var tabletransfer = frappe.model.get_doc("Maintenance Processing", frm.doc.maintenance_processing);
            $.each(tabletransfer.spare_parts, function(index, row){
                var d = frm.add_child("items");
                d.item_code = row.item_code;
                d.qty = row.qty;
            d.rate = row.rate;
            d.amount = row.amount;
            });
        cur_frm.refresh_field("items");
            });
}
});*/



frappe.ui.form.on("Maintenance Material Receipt Table", {
    "item_code": function (frm, cdt, cdn) {
        var d2 = locals[cdt][cdn];
        if (d2.item_code) {
            frappe.call({
                "method": "maintenance_system.maintenance_system.doctype.maintenance_directing.maintenance_directing.getPrice",
                args: {
                    item_code: d2.item_code
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.model.set_value(d2.doctype, d2.name, "rate", r.message[0][0]);
                        frappe.model.set_value(d2.doctype, d2.name, "uom", r.message[0][1]);
                    } else {
                        frappe.throw("Please Check Maintenance System Setting and Set Default Price List and Create an Item Price")
                    }
                }
            });
        }
    }
});



frappe.ui.form.on("Maintenance Material Receipt", {
    refresh: function (frm) {
        frm.trigger("onload")
    },
    onload: function (frm) {
        if(frm.doc.docstatus < 1 && !frm.doc.branch){
            frappe.call({
                "method": "maintenance_system.maintenance_system.doctype.maintenance_order.maintenance_order.order_default_branch",
                args:{
                    processing:frm.doc.processing,
                    doctype:frm.doc.processing.includes("EXT") ? "External Processing": "Internal Processing"
                },
                callback: function (r) {
                    frm.set_value("branch",r.message)
                    cur_frm.save()
                }
            });
        }
        
        // frappe.call({
        //     "method": "maintenance_system.maintenance_system.doctype.maintenance_material_receipt.maintenance_material_receipt.get_warehouse",
        //     callback: function (r) {
        //         frm.set_value("warehouse", r.message);
        //     }
        // });
    }
});



frappe.ui.form.on("Maintenance Material Receipt Table", "qty", function (frm, cdt, cdn) {

    var d = locals[cdt][cdn];
    frappe.model.set_value(d.doctype, d.name, "amount", d.qty * d.rate);
    var material = frm.doc.items;
    var total = 0
    for (var j in material) {
        total = total + material[j].amount
        frm.set_value("total", total);
    }
});

frappe.ui.form.on("Maintenance Material Receipt Table", "rate", function (frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.model.set_value(d.doctype, d.name, "amount", d.qty * d.rate);
    var material = frm.doc.items;
    var total = 0
    for (var j in material) {
        total = total + material[j].amount
        frm.set_value("total", total);
    }
});

//Check Actual Quantity

frappe.ui.form.on("Maintenance Material Receipt", "warehouse", function(frm) {
    frm.doc.items.forEach(function(d) { 
        frappe.call('maintenance_system.maintenance_system.doctype.maintenance_material_receipt.maintenance_material_receipt.update_actual', {
            item_code:d.item_code,warehouse:frm.doc.warehouse
        }).then(r => {
            frappe.model.set_value("Maintenance Material Receipt Table",d.name,"availability",r.message);

        })
    });
    cur_frm.refresh_fields("items");
    
});

frappe.ui.form.on("Maintenance Material Receipt Table", "item_code", function(frm,cdt, cdn) {
    var d = locals[cdt][cdn];
    frappe.call('maintenance_system.maintenance_system.doctype.maintenance_material_receipt.maintenance_material_receipt.update_actual', {
        item_code:d.item_code,warehouse:frm.doc.warehouse
    }).then(r => {
        frappe.model.set_value(cdt,cdn,"availability",r.message);
        cur_frm.refresh_fields("items");
    })
    
});



frappe.ui.form.on("Maintenance Material Receipt Table", "items_remove", function (frm, cdt, cdn) {

    var d = locals[cdt][cdn];
    var material = frm.doc.items;
    var total = 0
    for (var j in material) {
        total = total + material[j].amount
        frm.set_value("total", total);
    }
});

cur_frm.set_query("item_code", "items", function (doc, cdt, cdn) {
    var d = locals[cdt][cdn];
    return {
        filters: [
            ['Item', 'is_stock_item', '=', 1],
            ['Item', 'disabled', '=', 0],
            ['Item', 'is_sales_item', '=', 1]
        ]
    };
});

frappe.ui.form.on("Maintenance Material Receipt", "onload", function (frm) {
    if(frm.doc.docstatus < 1){
        frm.set_value("delivery_date",frappe.datetime.get_today())
    }

});
frappe.ui.form.on("Maintenance Material Receipt", "edit_delivery_date", function (frm) {
    if(frm.doc.edit_delivery_date == 1){
        frm.set_df_property("delivery_date","read_only",0)
    }else{
        frm.set_df_property("delivery_date","read_only",1)
    }
});