from __future__ import annotations
from dataclasses import dataclass

from . import OBSERVATION_ACTIONS, ORDER_ACTIONS

@dataclass(frozen=True)
class WorkTag:
    tag_id: str
    branch_id: str
    kind: str
    active: bool=True

def can_close(branch_id: str, tags: list[WorkTag], visible_breaks: set[str], grounded_sections: set[str]) -> tuple[bool,list[str]]:
    reasons=[]
    active=[t for t in tags if t.active and t.branch_id==branch_id]
    if any(t.kind in {"hold","clearance","do_not_operate"} for t in active): reasons.append("active_work_tag")
    if branch_id in visible_breaks: reasons.append("visible_break_required")
    if branch_id in grounded_sections: reasons.append("section_grounded")
    return (not reasons,reasons)

def validate_sequence(operations: list[tuple[str,str]], tags: list[WorkTag], visible_breaks: set[str], grounded_sections: set[str]):
    violations=[]
    for idx,(action,branch_id) in enumerate(operations):
        if action not in ORDER_ACTIONS:
            violations.append((idx,branch_id,("unknown_action",)))
        elif action=="close":
            ok,reasons=can_close(branch_id,tags,visible_breaks,grounded_sections)
            if not ok: violations.append((idx,branch_id,tuple(reasons)))
        # "open" is always permitted; verify/test are passive observation
        # steps that never change device state, so they need no interlock.
    return violations
