import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# ? These methods are first created in their respective views. They are then imported to init.py and then they are imported to request_handler.py.
from repository import all, delete, retrieve, create, update

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    # ? This is a Docstring it should be at the beginning of all classes and functions
    # ? It gives a description of the class or function

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # ? Try to get the item at index 2
        try:
            # ? Convert the string "1" to the integer 1
            # ? This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # ? This is a tuple

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = retrieve(id, resource)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ""
        else:
            self._set_headers(200)
            response = all(resource)

        return response

    # ? Here's a method on the class that overrides the parent's method.
    # ? It handles any GET request.

    def do_GET(self):
        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())

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
                and "species" in post_body
                and "locationId" in post_body
                and "customerId" in post_body
                and "status" in post_body
            ):
                self._set_headers(201)
                new_animal = create(resource, post_body)

            else:
                self._set_headers(400)
                new_animal = {
                    "message": f'{"name key is required. Check your data and try again." if "name" not in post_body else ""} {"species key is required. Check your data and try again. " if "species" not in post_body else ""} {"locationId key is required. Check your data and try again." if "locationId" not in post_body else ""} {"customerId key is required. Check your data and try again. " if "customerId" not in post_body else ""} {"status key is required. Check your data and try again. " if "status" not in post_body else ""}'
                }

            #! Encode the new animal and send in response
            self.wfile.write(json.dumps(new_animal).encode())

        # ? If the resource == "locations", and if the "name" key and  "address" key are present in the post_body dictionary, than the request will have a header of 201, and a new location will be created.
        # ? Else/Otherwise, the request header will be set to 400, and a message will be stored inside of the new location variable. Message is a ternary statement in python. If the "name" key is not in post_body dictionary, then the message will be "name is required", else an empty string will be returned. If the "address" key is not in post_body dictionary, then the message will be "address is required", else an empty string will be returned.
        if resource == "locations":
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_location = create(resource, post_body)

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
                new_employee = create(resource, post_body)

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
                new_customer = create(resource, post_body)

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
            delete(id, resource)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        elif resource == "locations":
            self._set_headers(204)
            delete(id, resource)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        if resource == "employees":
            self._set_headers(204)
            delete(id, resource)

        # Encode the new animal and send in response

        # Delete a single animal from the list
        if resource == "customers":
            self._set_headers(405)
            delete_response = {"message": "You cannot delete any customer."}

        # Encode the new anitmal and send in response

        self.wfile.write(json.dumps(delete_response).encode())
        # self.wfile.write(delete_response.encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update(id, post_body, resource)

            # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "locations":
            update(id, post_body, resource)

            # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "employees":
            update(id, post_body, resource)

            # Encode the new animal and send in response
            self.wfile.write("".encode())

        # Delete a single animal from the list
        if resource == "customers":
            update(id, post_body, resource)

            # Encode the new animal and send in response
            self.wfile.write("".encode())

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
        # any domain on the internet can send my a request
        # if I changed the second parameter is locahost/3000, then only
        self.send_header("Access-Control-Allow-Origin", "*")
        # allows only these methods below to take place.
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        # controlling what headers the client is allowed to put on their request.
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
