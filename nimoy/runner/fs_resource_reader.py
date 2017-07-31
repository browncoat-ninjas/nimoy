def read(resource_location):
    with open(resource_location, 'r') as resource:
        text = resource.read()
    return text
