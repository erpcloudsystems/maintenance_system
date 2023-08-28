// Copyright (c) 2020, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Warranty Template', {
	onload: function(frm) {
        if (!frappe.user_roles.includes("System Manager")) {
            cur_frm.set_df_property("warranty_bearing_rate", "read_only", 1 )
            cur_frm.set_df_property("warranty_period_type", "read_only", 1 )
            cur_frm.set_df_property("warranty_period", "read_only", 1 )
        }
	}
});

// frappe.ui.form.on('Warranty Bearing Rate', {
// 	onload: function(frm,cdt,cdn) {
//         if (!frappe.user_roles.includes("System Manager")) {
//             var df = frappe.meta.get_docfield("Warranty Bearing Rate","repairing_tolerance", cdn);
//             df.read_only = 1;
//         }
// 	}
// });