import time

def check_rate_limit(client_id, request_counts, rate_limit_lock):
    """Check if client has exceeded rate limit"""
    with rate_limit_lock:
        current_time = time.time()
        # Remove requests older than 60 seconds
        request_counts[client_id] = [
            req_time for req_time in request_counts[client_id]
            if current_time - req_time < 60
        ]

        if len(request_counts[client_id]) >= 10:  # MAX_REQUESTS_PER_MINUTE
            return False

        request_counts[client_id].append(current_time)
        return True
