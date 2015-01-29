# -*- coding: utf-8 -*-
"""
helper functions
"""
# ============================================================================
#                        NECESSARY IMPORTS
# ============================================================================
import string
import random


# ============================================================================
#                    HELPER FUNCTIONS DEFINITIONS
# ============================================================================
def random_string():
    """
    Generate 16 Characters Random String

    Args: None

    Kwargs: None

    Returns:
        rs (str): random string

    Raises: None

    """
    rs = (''.join(random.choice(string.ascii_uppercase)
                  for i in range(16)))
    return rs

# ============================================================================
#                              EOF
# ============================================================================
