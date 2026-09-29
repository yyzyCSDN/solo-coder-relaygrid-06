from __future__ import annotations

# Unified action vocabulary shared by switching orders, interlocks, and the
# command bus. Actions split into two kinds:
#   * state-changing commands (open/close/trip/reset) that move a device;
#   * observation steps (verify/test) that only read or check a state and
#     therefore must never be treated as interlocking violations.
DEVICE_COMMANDS = frozenset({"open", "close", "trip", "reset"})
OBSERVATION_STEPS = frozenset({"verify", "test"})
SWITCHING_ACTIONS = DEVICE_COMMANDS | OBSERVATION_STEPS
