#utility functions

import string
import random

def random_id_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

