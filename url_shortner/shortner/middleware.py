from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class CustomLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        method = request.method
        path = request.get_full_path()
        body = request.body.decode('utf-8') if request.body else ''

        log_entry = f"[{timezone.now()}] {method} {path} BODY: {body}\n"

        # Write to a custom log file
        with open("request_logs.txt", "a") as log_file:
            log_file.write(log_entry)
