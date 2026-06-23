import random
import string

def generate_code():
    prefix = "EVT-2026-"

    chars = string.ascii_uppercase + string.digits

    suffix = "".join(random.choices(chars, k=6))

    return prefix + suffix