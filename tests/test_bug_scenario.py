from relaygrid.operations.command_bus import Command, CommandBus
from relaygrid.switching.interlocks import validate_sequence
from relaygrid.switching.orders import OrderState, SwitchingOrder, SwitchingStep


def test_switching_verification_and_terminal_retries_are_idempotent():
    operations = [("verify", "SW1"), ("open", "SW1"), ("test", "SW1")]
    assert validate_sequence(operations, [], set(), set()) == []

    order = SwitchingOrder("O1")
    order.create(
        [
            SwitchingStep(1, "verify", "SW1", "closed"),
            SwitchingStep(2, "open", "SW1", "open"),
        ],
        author="author",
    )
    order.check("checker")
    order.approve("approver")
    order.start()
    order.acknowledge(1, "operator", 1.0)
    order.acknowledge(2, "operator", 2.0)
    order.acknowledge(2, "operator", 2.0)
    assert order.current.state == OrderState.COMPLETE
    assert order.acknowledgements == {1: ("operator", 1.0), 2: ("operator", 2.0)}

    bus = CommandBus()
    command = Command("C1", "SW1", "open", 0.0, 60.0, "operator")
    bus.submit(command, now=0.0)
    assert bus.next_for("SW1", now=1.0) == command
    bus.complete(command, "success", 2.0, "open")
    bus.complete(command, "failed", 3.0, "closed")
    assert bus.completed["C1"].status == "success"
    assert bus.completed["C1"].observed_state == "open"
