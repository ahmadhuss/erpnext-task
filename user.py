import frappe
from frappe.model.document import Document


class User(Document):
    pass


@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["GET"])
def get_users_list():
    
    if not frappe.request.method == "GET":
        return frappe.as_json({"error": _("Invalid request method: {}".format(frappe.request.method))})

    users = frappe.get_all("User", {"enabled": 1})
    return frappe.as_json(users)

@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["POST"])
def update_user_name(email, first_name, last_name):
    
    if not frappe.request.method == "POST":
            return frappe.as_json({"error": _("Invalid request method: {}".format(frappe.request.method))})

    if frappe.db.exists("User", {"email": email}):
        user = frappe.get_doc("User", {"email": email})
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        response = {
            "id": user.name,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        return frappe.as_json(response)
    else:
        return frappe.as_json({"error": "User not found"})
