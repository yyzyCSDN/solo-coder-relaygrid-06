from __future__ import annotations

# Actions that change device state and are subject to interlocking.
SWITCHING_ACTIONS = frozenset({"open", "close"})
# Passive steps that observe or probe a device without changing its state.
# They are valid steps in an order/sequence but carry no interlock checks.
OBSERVATION_ACTIONS = frozenset({"verify", "test"})
# Every action accepted by an operation order or a sequence validation.
ORDER_ACTIONS = frozenset(SWITCHING_ACTIONS | OBSERVATION_ACTIONS)

__all__ = [
    "SWITCHING_ACTIONS",
    "OBSERVATION_ACTIONS",
    "ORDER_ACTIONS",
]
