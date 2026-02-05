from .models import BodyShape, BodyShapeResult, Gender, Measurements


def _within_percent(a: float, b: float, pct: float) -> bool:
    if b == 0:
        return True
    diff = abs(a - b) / b
    return diff <= pct / 100.0


def _waist_smaller_than(waist: float, other: float, min_pct: float) -> bool:
    if other == 0:
        return False
    return waist <= other * (1 - min_pct / 100.0)


def get_body_shape_from_measurements(m: Measurements, gender: Gender = Gender.female) -> BodyShapeResult:
    shoulder, waist, hip = m.shoulder, m.waist, m.hip
    max_val = max(shoulder, waist, hip)
    if max_val == 0:
        return BodyShapeResult(
            shape=BodyShape.rectangle,
            confidence=0.0,
            reasoning="Please enter valid measurements.",
        )

    if gender == Gender.male:
        if shoulder >= waist * 1.2 and shoulder >= hip * 1.15:
            return BodyShapeResult(
                shape=BodyShape.inverted_triangle,
                confidence=0.9,
                reasoning=f"Your shoulders ({shoulder}) are significantly broader than your waist ({waist}) and hips ({hip}), "
                "creating a strong V-shape (inverted triangle).",
            )

        if shoulder >= waist * 1.1 and shoulder >= hip * 1.05 and waist <= hip * 1.05:
            return BodyShapeResult(
                shape=BodyShape.trapezoid,
                confidence=0.88,
                reasoning=f"Your shoulders ({shoulder}) are broader than your waist ({waist}) and hips ({hip}) in a balanced way—"
                "typical of a trapezoid (athletic) frame.",
            )

        if hip > shoulder * 1.08 or waist > shoulder * 1.05:
            return BodyShapeResult(
                shape=BodyShape.triangle,
                confidence=0.86,
                reasoning=f"Your lower body or midsection ({waist}–{hip}) is wider than your shoulders ({shoulder}), giving a triangle frame.",
            )

        if waist >= shoulder * 1.05 and waist >= hip * 1.05:
            return BodyShapeResult(
                shape=BodyShape.apple,
                confidence=0.86,
                reasoning=f"Your waist ({waist}) is your most prominent measurement compared with shoulders ({shoulder}) and hips ({hip}), "
                "which is typical of an oval/apple frame.",
            )

        return BodyShapeResult(
            shape=BodyShape.rectangle,
            confidence=0.82,
            reasoning=f"Your shoulders ({shoulder}), waist ({waist}), and hips ({hip}) are relatively even, creating a rectangle frame.",
        )

    if (
        _within_percent(shoulder, hip, 8)
        and _waist_smaller_than(waist, shoulder, 20)
        and _waist_smaller_than(waist, hip, 20)
    ):
        return BodyShapeResult(
            shape=BodyShape.hourglass,
            confidence=0.92,
            reasoning=f"Your shoulder ({shoulder}) and hip ({hip}) measurements are balanced, with a defined waist ({waist}) "
            "that’s noticeably smaller—creating a classic hourglass silhouette.",
        )

    if hip > shoulder * 1.05:
        return BodyShapeResult(
            shape=BodyShape.pear,
            confidence=0.88,
            reasoning=f"Your hips ({hip}) are wider than your shoulders ({shoulder}), with a proportionally smaller upper body—"
            "characteristic of a pear shape.",
        )

    if shoulder > hip * 1.05:
        return BodyShapeResult(
            shape=BodyShape.inverted_triangle,
            confidence=0.88,
            reasoning=f"Your shoulders ({shoulder}) are broader than your hips ({hip}), creating a strong upper frame—"
            "an inverted triangle shape.",
        )

    if waist >= shoulder * 0.95 or waist >= hip * 0.95:
        return BodyShapeResult(
            shape=BodyShape.apple,
            confidence=0.85,
            reasoning=f"Your waist ({waist}) is close to or matches your shoulder and hip measurements, "
            "with weight carried through the midsection—an apple shape.",
        )

    if (
        _within_percent(shoulder, waist, 15)
        and _within_percent(waist, hip, 15)
        and _within_percent(shoulder, hip, 15)
    ):
        return BodyShapeResult(
            shape=BodyShape.rectangle,
            confidence=0.86,
            reasoning=f"Your shoulder ({shoulder}), waist ({waist}), and hip ({hip}) measurements are relatively similar, "
            "giving a balanced rectangular silhouette.",
        )

    return BodyShapeResult(
        shape=BodyShape.rectangle,
        confidence=0.7,
        reasoning=f"Your proportions are closest to a rectangular shape: shoulder {shoulder}, waist {waist}, hip {hip}.",
    )

