from correction_transport_gate import TransportCell, evaluate_correction_transport


def main() -> None:
    validated = (
        TransportCell("camera-A", "position-NF"),
        TransportCell("camera-A", "position-SF"),
    )
    inside = evaluate_correction_transport(
        hardware="camera-A",
        observation_context="position-NF",
        validated_cells=validated,
        validation_passed=True,
    )
    assert inside.admissible

    new_hardware = evaluate_correction_transport(
        hardware="camera-B",
        observation_context="position-NF",
        validated_cells=validated,
        validation_passed=True,
    )
    assert not new_hardware.admissible
    assert new_hardware.reason == "query_outside_validated_transport_domain"

    new_context = evaluate_correction_transport(
        hardware="camera-A",
        observation_context="position-NEW",
        validated_cells=validated,
        validation_passed=True,
    )
    assert not new_context.admissible

    failed_validation = evaluate_correction_transport(
        hardware="camera-A",
        observation_context="position-NF",
        validated_cells=validated,
        validation_passed=False,
    )
    assert not failed_validation.admissible
    assert failed_validation.reason == "validation_not_passed"

    print("REC correction transport gate verified.")


if __name__ == "__main__":
    main()
