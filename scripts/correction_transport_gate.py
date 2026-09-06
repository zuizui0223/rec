"""Fail-closed transport gate for REC entry-aware correction.

The gate does not estimate a correction model. It only decides whether a query
falls inside an explicitly validated correction-transport domain.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, order=True)
class TransportCell:
    hardware: str
    observation_context: str


@dataclass(frozen=True)
class CorrectionTransportGate:
    query: TransportCell
    validated_cells: tuple[TransportCell, ...]
    validation_passed: bool
    admissible: bool
    reason: str


def evaluate_correction_transport(
    *,
    hardware: str,
    observation_context: str,
    validated_cells: Iterable[TransportCell],
    validation_passed: bool,
) -> CorrectionTransportGate:
    """Allow correction only inside an explicitly validated transport cell."""
    query = TransportCell(str(hardware), str(observation_context))
    cells = tuple(validated_cells)
    if not cells:
        return CorrectionTransportGate(
            query, cells, bool(validation_passed), False, "no_validated_transport_cells"
        )
    if not validation_passed:
        return CorrectionTransportGate(
            query, cells, False, False, "validation_not_passed"
        )
    if query not in cells:
        return CorrectionTransportGate(
            query, cells, True, False, "query_outside_validated_transport_domain"
        )
    return CorrectionTransportGate(
        query, cells, True, True, "query_inside_validated_transport_domain"
    )
