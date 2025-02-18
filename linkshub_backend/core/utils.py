def get_request_data(request):
    # Extract data from the request based on its method
    is_body = bool(request.body)
    data = ''
    if request.method == 'GET' and not is_body:
        data = request.GET
        return data
    data = request.data
    return data