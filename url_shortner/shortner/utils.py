
import random, string

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_location_from_ip(ip):
    
    return "Unknown Location"
