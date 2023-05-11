import requests

session = requests.Session()


class Roblox_API:
    def roblox_request(self, method, url, **kwargs):  # accepts htp method, api_endpoint, and var args
        request = session.request(method, url, **kwargs)  # makes the request
        method = method.lower()
        if (method == "post") or (method == "put") or (method == "patch") or (
                method == "delete"):  # checks for these requests
            if "X-CSRF-TOKEN" in request.headers:
                session.headers["X-CSRF-TOKEN"] = request.headers["X-CSRF-TOKEN"]
                if request.status_code == 403:  # Request failed, send it again
                    request = session.request(method, url, **kwargs)
        return request
