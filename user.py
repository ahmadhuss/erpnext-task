import frappe
from frappe.model.document import Document
import json

class User(Document):
    pass


@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["GET"])
def get_users_list():
    # Gets documents from the database with filter 'enabled:true' 
    try:
        all_users = frappe.db.get_list('User',
            filters={
            'enabled': True
            },
            as_dict=True
        )
        return json.dumps(all_users)
    except frappe.db.Error as e:
        return json.dumps({"status": "failed", "message": str(e)})

@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["POST"])
def update_user_name(email, first_name, last_name):
    try:
        user_available = frappe.db.exists("User", {"email": email})

        if user_available:
            user = frappe.get_doc({
                'doctype': "User",
                'email': email
            })
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            #converting the doc to dictionary
            doc_dict = user.as_dict()

            # Convert dictionary to JSON string
            return frappe.as_json(doc_dict)
    except frappe.db.Error as e:
        return json.dumps({"status": "failed", "message": str(e)})

