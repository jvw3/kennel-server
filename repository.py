DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 4,
            "status": "Admitted",
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted",
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted",
        },
    ],
    "locations": [
        {"id": 1, "name": "Nashville North", "address": "8422 Johnson Pike"},
        {"id": 2, "name": "Nashville South", "address": "209 Emory Drive"},
    ],
    "customers": [{"id": 1, "fullName": "Ryan Tanay", "email": "Tanay@gmail.com"}],
    "employees": [{"id": 1, "name": "Jenna Solis"}],
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(id, resource):
    """For GET requests to a single resource"""
    requested_data = None

    for data in DATABASE[resource]:
        if data["id"] == id:
            requested_data = data

            if resource == "animals":

                matching_location = retrieve(requested_data["locationId"], "locations")
                requested_data["location"] = matching_location

                matching_customer = retrieve(requested_data["customerId"], "customers")
                requested_data["customer"] = matching_customer

                del requested_data["locationId"]
                del requested_data["customerId"]

    return requested_data


def create(resource, newdata):
    """For POST requests to a collection"""

    max_id = DATABASE[resource][-1]["id"]

    new_id = max_id + 1

    newdata["id"] = new_id

    DATABASE[resource].append(newdata)

    return newdata


def update(id, updated_data, resource):
    """For PUT requests to a single resource"""
    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            # Found the animal. Update the value.
            DATABASE[resource][index] = updated_data
            break


def delete(id, resource):
    """For DELETE requests to a single resource"""
    data_index = -1

    for index, data in enumerate(DATABASE[resource]):
        if data["id"] == id:
            # Found the animal. Store the current index.
            data_index = index

    if data_index >= 0:
        DATABASE[resource].pop(data_index)
