import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# ? These methods are first created in their respective views. They are then imported to init.py and then they are imported to request_handler.py.

from views import (
    get_all_animals,
    get_single_animal,
    get_all_locations,
    get_single_location,
    get_all_employees,
    get_single_employee,
    get_all_customers,
    get_single_customer,
    create_animal,
    create_location,
    create_employee,
    create_customer,
    delete_animal,
    delete_location,
    delete_employee,
    delete_customer,
    update_animal,
    update_customer,
    update_employee,
    update_location,
    get_customer_by_email,
    get_animal_by_location,
    get_employee_by_location,
    get_animal_by_status,
)
from views.animal_requests import get_animal_by_location


method_mapper = {
    "animals": {"single": get_single_animal, "all": get_all_animals},
    "locations": {"single": get_single_location, "all": get_all_locations},
    "customers": {"single": get_single_customer, "all": get_all_customers},
    "employees": {"single": get_single_employee, "all": get_all_employees},
}
# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    # ? This is a Docstring it should be at the beginning of all classes and functions
    # ? It gives a description of the class or function

    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ""
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response

    # ? Here's a method on the class that overrides the parent's method.
    # ? It handles any GET request.

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if "?" not in self.path:
            (resource, id) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get("email") and resource == "customers":
                response = get_customer_by_email(query["email"][0])

            if query.get("location_id") and resource == "animals":
                response = get_animal_by_location(query["location_id"][0])

            if query.get("status") and resource == "animals":
                response = get_animal_by_status(query["status"][0])

            if query.get("location_id") and resource == "employees":
                response = get_employee_by_location(query["location_id"][0])

        self.wfile.write(response.encode())
        # response = None
        # (resource, id) = self.parse_url(self.path)
        # response = self.get_all_or_single(resource, id)
        # self.wfile.write(json.dumps(response).encode())

    # def do_GET(self):
    #     """Handles GET requests to the server"""
    #     self._set_headers(200)
    #     response = {}  # Default response

    #     #! Parse the URL and capture the tuple that is returned
    #     (resource, id) = self.parse_url(self.path)

    #     # ? If the resource is "animals", and
    #     # ? if id is not None/Null, the response will be get_single_animal(id)
    #     # ? if the response is not None/Null, the request header will be set to 200.
    #     # ? if the response is None/Null, the request header will be set to 404. and the response will be a message.
    #     # ? else, the response will be the return value of the get_all_animals method.
    #     if resource == "animals":
    #         if id is not None:
    #             response = get_single_animal(id)

    #             if response is not None:
    #                 self._set_headers(200)

    #             if response is None:
    #                 self._set_headers(404)
    #                 response = {"message": f"Animal {id} is out playing right now"}

    #         else:
    #             response = get_all_animals()

    #     # ? If the resource is "locations", and
    #     # ? if id is not None/Null, the response will be get_single_location(id)
    #     # ? if the response is not None/Null, the request header will be set to 200.
    #     # ? if the response is None/Null, the request header will be set to 404. and the response will be a message.
    #     # ? else, the response will be the return value of the get_all_locations method.
    #     if resource == "locations":
    #         if id is not None:
    #             response = get_single_location(id)

    #             if response is not None:
    #                 self._set_headers(200)

    #             if response is None:
    #                 self._set_headers(404)
    #                 response = {"message": f"Location-{id} doesn't exist"}

    #         else:
    #             response = get_all_locations()

    #     # ? If the resource is "employees", and
    #     # ? if id is not None/Null, the response will be get_single_employee(id)
    #     # ? if the response is not None/Null, the request header will be set to 200.
    #     # ? if the response is None/Null, the request header will be set to 404. and the response will be a message.
    #     # ? else, the response will be the return value of the get_all_employees method.
    #     if resource == "employees":
    #         if id is not None:
    #             response = get_single_employee(id)

    #             if response is not None:
    #                 self._set_headers(200)

    #             if response is None:
    #                 self._set_headers(404)
    #                 response = {"message": f"Employee-{id} does not exist"}

    #         else:
    #             response = get_all_employees()

    #     # ? If the resource is "animals", and
    #     # ? if id is not None/Null, the response will be get_single_animal(id)
    #     # ? if the response is not None/Null, the request header will be set to 200.
    #     # ? if the response is None/Null, the request header will be set to 404. and the response will be a message.
    #     # ? else, the response will be the return value of the get_all_animals method.
    #     if resource == "customers":
    #         if id is not None:
    #             response = get_single_customer(id)

    #             if response is not None:
    #                 self._set_headers(200)

    #             if response is None:
    #                 self._set_headers(404)
    #                 response = {"message": f"Customer-{id} does not exist"}

    #         else:
    #             response = get_all_customers()

    #     self.wfile.write(json.dumps(response).encode())

    #! Here's a method on the class that overrides the parent's method.
    # ? It handles any POST request.
    def do_POST(self):
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)

        # ? Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        #! Parse the URL
        (resource, id) = self.parse_url(self.path)

        # ? Initialize new animal
        new_animal = None
        # ? Initialize new employee
        new_employee = None
        # ? Initialize new location
        new_location = None
        # ? Initialize new customer
        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        # ? Below is the logic for how new resources will be created and added to the API.
        if resource == "animals":
            if (
                "name" in post_body
                and "breed" in post_body
                and "location_id" in post_body
                and "customer_id" in post_body
                and "status" in post_body
            ):
                self._set_headers(201)
                new_animal = create_animal(post_body)

            else:
                self._set_headers(400)
                new_animal = {
                    "message": f'{"name key is required. Check your data and try again." if "name" not in post_body else ""} {"breed key is required. Check your data and try again. " if "breed" not in post_body else ""} {"location_id key is required. Check your data and try again." if "location_id" not in post_body else ""} {"customer_id key is required. Check your data and try again. " if "customer_id" not in post_body else ""} {"status key is required. Check your data and try again. " if "status" not in post_body else ""}'
                }

            #! Encode the new animal and send in response
            self.wfile.write(json.dumps(new_animal).encode())

        # ? If the resource == "locations", and if the "name" key and  "address" key are present in the post_body dictionary, than the request will have a header of 201, and a new location will be created.
        # ? Else/Otherwise, the request header will be set to 400, and a message will be stored inside of the new location variable. Message is a ternary statement in python. If the "name" key is not in post_body dictionary, then the message will be "name is required", else an empty string will be returned. If the "address" key is not in post_body dictionary, then the message will be "address is required", else an empty string will be returned.
        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create_location(post_body)

            else:
                self._set_headers(400)
                new_location = {
                    "message": f'{"name key is required. Check your data and try again." if "name" not in post_body else ""} {"address is required. Check your data and try again." if "address" not in post_body else ""}'
                }

            #! Encode the new animal and send in response
            self.wfile.write(json.dumps(new_location).encode())

        # ? If the resource == "employees", and if the "name" key is present in the post_body dictionary, than the request will have a header of 201, and a new employee will be created.
        # ? Else/Otherwise, the request header will be set to 400, and a message will be stored inside of the new employee variable. Message is a ternary statement in python. If the "name" key is not in post_body dictionary, then the message will be "name is required", else an empty string will be returned.
        if resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                new_employee = create_employee(post_body)

            else:
                self._set_headers(400)
                new_employee = {
                    "message": f'{"name key is required. Check your data and try again." if "name" not in post_body else ""}'
                }

            self.wfile.write(json.dumps(new_employee).encode())

        # ? If the resource == "locations", and if the "name" key and  "address" key are present in the post_body dictionary, than the request will have a header of 201, and a new location will be created.
        # ? Else/Otherwise, the request header will be set to 400, and a message will be stored inside of the new location variable. Message is a ternary statement in python. If the "name" key is not in post_body dictionary, then the message will be "name is required", else an empty string will be returned. If the "address" key is not in post_body dictionary, then the message will be "address is required", else an empty string will be returned.
        if resource == "customers":
            if "fullName" in post_body and "email" in post_body:
                self._set_headers(201)
                new_customer = create_customer(post_body)

            else:
                self._set_headers(400)
                new_customer = {
                    "post_request_failed": f'{"fullName key is required. Check your data and try again." if "fullName" not in post_body else ""} {"email key is required. Check your data and try again." if "email" not in post_body else ""}'
                }

            self.wfile.write(json.dumps(new_customer).encode())

    def do_DELETE(self):
        # Set a 204 response code
        delete_response = ""

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            self._set_headers(204)
            delete_animal(id)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        elif resource == "locations":
            self._set_headers(204)
            delete_location(id)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        if resource == "employees":
            self._set_headers(204)
            delete_employee(id)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        if resource == "customers":
            self._set_headers(405)
            delete_response = {"message": "You cannot delete any customer."}
            # delete_customer(id)

        # Encode the new anitmal and send in response

        self.wfile.write(json.dumps(delete_response).encode())
        # self.wfile.write(delete_response.encode())

    def do_PUT(self):
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)

        elif resource == "locations":
            update_location(id, post_body)
        # rest of the elif's
        elif resource == "employees":
            update_employee(id, post_body)

        elif resource == "customers":
            update_customer(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    # A method that handles any PUT request.

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        # is your domain on the list to access API.
        self.send_header("Access-Control-Allow-Origin", "*")
        # is user allowed to perform this action on the API.
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()

# ? content type is telling what type of string we are sending. We are always sending a string.
# ? Accept header can control the format in which the client can accept the request.
