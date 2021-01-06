"""
Secret sharing scheme.
"""

from __future__ import annotations

from typing import List


class Share:
    """
    A secret share in a finite field.
    """

    def __init__(self, *args, **kwargs):
        # Adapt constructor arguments as you wish
        raise NotImplementedError("You need to implement this method.")

    def __repr__(self):
        # Helps with debugging.
        raise NotImplementedError("You need to implement this method.")

    def __add__(self, other):
        raise NotImplementedError("You need to implement this method.")

    def __sub__(self, other):
        raise NotImplementedError("You need to implement this method.")

    def __mul__(self, other):
        raise NotImplementedError("You need to implement this method.")

    def serialize(self):
        """Generate a representation suitable for passing in a message."""
        raise NotImplementedError("You need to implement this method.")

    @staticmethod
    def deserialize(serialized) -> Share:
        """Restore object from its serialized representation."""
        raise NotImplementedError("You need to implement this method.")


def share_secret(secret: int, num_shares: int) -> List[Share]:
    """Generate secret shares."""
    raise NotImplementedError("You need to implement this method.")


def reconstruct_secret(shares: List[Share]) -> int:
    """Reconstruct the secret from shares."""
    raise NotImplementedError("You need to implement this method.")


# Feel free to add as many methods as you want.
