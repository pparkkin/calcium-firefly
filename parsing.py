
import json

def with_json_body(f):
    def w(*args, **kwargs):
        self = args[0]
        b = self.request.body
        try:
            r = json.loads(b)
        except Exception:
            self.response.status = 400
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({"error": "Unable to parse request"}))
            return
        return f(self, r, *args[1:], **kwargs)
    return w
