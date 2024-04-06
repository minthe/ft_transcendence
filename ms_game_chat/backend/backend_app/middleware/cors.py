class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming Origin header
        # origin = request.META.get('HTTP_ORIGIN', '')
        # print('Incoming Origin:', origin)

        response = self.get_response(request)

        # Allow all origins for simplicity; adjust as needed
        response["Access-Control-Allow-Origin"] = "*"

        # Handle OPTIONS requests
        if request.method == "OPTIONS":
            print(response)
            # Include any specific headers needed for the OPTIONS request
            response["Access-Control-Allow-Origin"] = "*"
        return response
