import frappe
from frappe.model.document import Document
import json

class User(Document):
    pass


@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["GET"])
@frappe.api.validate_request
def get_users_list():
    # Get all enabled users from the User doctype
    users = frappe.get_list("User", filters={"enabled": 1}, fields=["name", "email", "first_name", "last_name"])
    
    # Convert the users to a list of dictionaries
    user_list = []
    for user in users:
        user_dict = {
            "name": user.name,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        user_list.append(user_dict)

	# Return the list of users as a JSON response
    return json.dumps(user_list)    



@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["POST"])
@frappe.api.validate_request
def update_user_name(email, first_name, last_name):
    # Get the request data
    data = frappe.request.get_json()
    
    # Get the user from the User doctype with the given email
    user = frappe.get_doc("User", {"email": data.get("email")})
    
    # If the user is found, update their details
    if user:
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.save()
        
        # Convert the updated user to a dictionary
        user_dict = {
            "name": user.name,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
        # Return the updated user as a JSON response
        return json.dumps(user_dict)
    else:
        # If the user is not found, return an error message
        error_dict = {"error": "User not found"}
        return json.dumps(error_dict)
    

# We can Also use like this

@frappe.whitelist(allow_guest=True, xss_safe=False, methods=["POST"])
@frappe.api.validate_request
def update_user_name(email, first_name, last_name):
    
    # Get the user from the User doctype with the given email
    user = frappe.get_doc("User", {"email": email})
    
    # If the user is found, update their details
    if user:
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Convert the updated user to a dictionary
        user_dict = {
            "name": user.name,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
        # Return the updated user as a JSON response
        return json.dumps(user_dict)
    else:
        # If the user is not found, return an error message
        error_dict = {"error": "User not found"}
        return json.dumps(error_dict)
