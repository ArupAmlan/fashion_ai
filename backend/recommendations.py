from dataclasses import dataclass
from typing import List

from .models import BodyShape, ColourPalette, Gender, OutfitSuggestion, Undertone


@dataclass
class SilhouetteRule:
    body_shapes: List[BodyShape]
    silhouette: str
    description: str
    reasoning: str


@dataclass
class OutfitTemplate:
    id: str
    name: str
    description: str
    body_shapes: List[BodyShape]
    colour_tags: dict[Undertone, List[str]]
    silhouette: str
    imageUrl: str = ""


SILHOUETTE_RULES_FEMALE: List[SilhouetteRule] = [
    SilhouetteRule(
        body_shapes=[BodyShape.hourglass],
        silhouette="Fitted waist, A-line skirts, wrap dresses",
        description="Structured waist definition and balanced proportions",
        reasoning="Define your natural waist; avoid boxy or oversized shapes that hide your curves.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.pear],
        silhouette="Structured shoulders, A-line skirts, dark bottoms",
        description="Balance hips with shoulder detail and streamlined lower half",
        reasoning="Add volume or detail at the shoulders; choose A-line or straight silhouettes for the lower body.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.inverted_triangle],
        silhouette="V-necks, flared bottoms, wide-leg trousers",
        description="Soften shoulders and add volume at hips",
        reasoning="Avoid heavy shoulder detail; use V-necks and flared or wide-leg styles to balance your frame.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.rectangle],
        silhouette="Layered tops, belted looks, peplum, ruffles",
        description="Create curves with layers and waist definition",
        reasoning="Add dimension with belts, peplum, or layered pieces to create the illusion of a defined waist.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.apple],
        silhouette="V-necks, empire waist, flowy fabrics, straight legs",
        description="Elongate torso and draw eyes to neckline and legs",
        reasoning="Empire lines and V-necks lengthen the torso; avoid tight waistbands; choose flowy fabrics.",
    ),
]

SILHOUETTE_RULES_MALE: List[SilhouetteRule] = [
    SilhouetteRule(
        body_shapes=[BodyShape.trapezoid],
        silhouette="Fitted tees, structured jackets, straight/athletic fit",
        description="Highlight shoulders while keeping lines clean",
        reasoning="A tailored fit through the torso enhances your athletic frame; avoid overly boxy cuts.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.inverted_triangle],
        silhouette="Open collars, minimal shoulder padding, tapered/straight trousers",
        description="Balance broad shoulders with clean lower-half volume",
        reasoning="Keep tops streamlined; add structure with straight or slightly wider-leg trousers to balance proportions.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.triangle],
        silhouette="Darker bottoms, structured shoulders, vertical layers",
        description="Draw attention upward and streamline the lower half",
        reasoning="Use jackets with structure and avoid overly tight bottoms; darker colours below create balance.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.apple],
        silhouette="V-necks, open overshirts, straight fits, longer layers",
        description="Lengthen the torso with vertical lines",
        reasoning="Choose comfortable, breathable fabrics with vertical layering; avoid tight waist emphasis.",
    ),
    SilhouetteRule(
        body_shapes=[BodyShape.rectangle],
        silhouette="Layering, overshirts, textured knits, tailored outerwear",
        description="Add dimension with layers and texture",
        reasoning="Use layering and texture to build shape; aim for tailored shoulders and clean waist lines.",
    ),
]


OUTFIT_TEMPLATES_FEMALE: List[OutfitTemplate] = [
    OutfitTemplate(
        id="wrap-dress",
        name="Wrap dress",
        description="A wrap dress that defines the waist and suits multiple occasions.",
        body_shapes=[BodyShape.hourglass, BodyShape.pear, BodyShape.rectangle],
        colour_tags={
            Undertone.warm: ["Camel", "Rust", "Olive green", "Terracotta"],
            Undertone.cool: ["Navy", "Plum", "Dusty rose", "Slate blue"],
            Undertone.neutral: ["Dusty rose", "Sage", "Navy", "Taupe"],
        },
        silhouette="Fitted waist, V-neck, flattering wrap",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20a%20wrap%20dress%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="structured-blazer",
        name="Structured blazer + tailored trousers",
        description="Sharp blazer with tailored trousers for a polished look.",
        body_shapes=[BodyShape.rectangle, BodyShape.pear, BodyShape.inverted_triangle],
        colour_tags={
            Undertone.warm: ["Camel", "Warm brown", "Olive", "Gold"],
            Undertone.cool: ["Navy", "Charcoal", "Slate blue", "Plum"],
            Undertone.neutral: ["Charcoal", "Navy", "Taupe", "Dusty rose"],
        },
        silhouette="Structured shoulders, clean lines",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20a%20structured%20blazer%20and%20tailored%20trousers%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="a-line-midi",
        name="A-line midi skirt + fitted top",
        description="A-line skirt that skims the hips with a fitted top.",
        body_shapes=[BodyShape.pear, BodyShape.hourglass, BodyShape.apple],
        colour_tags={
            Undertone.warm: ["Cream", "Terracotta", "Peach", "Olive green"],
            Undertone.cool: ["Cool pink", "Lavender", "Mint", "Ice blue"],
            Undertone.neutral: ["Blush", "Sage", "Mauve", "Soft white"],
        },
        silhouette="A-line skirt, fitted or tucked top",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20an%20A-line%20midi%20skirt%20and%20fitted%20top%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="v-neck-flowy",
        name="V-neck flowy top + straight-leg trousers",
        description="Flowing top with a V-neck and straight-leg trousers.",
        body_shapes=[BodyShape.apple, BodyShape.inverted_triangle, BodyShape.rectangle],
        colour_tags={
            Undertone.warm: ["Peach", "Coral", "Cream", "Terracotta"],
            Undertone.cool: ["Lavender", "Soft white", "Plum", "Mint"],
            Undertone.neutral: ["Blush", "Sage", "Soft white", "Mauve"],
        },
        silhouette="V-neck, flowy fabric, straight legs",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20a%20V-neck%20flowy%20top%20and%20straight-leg%20trousers%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="empire-waist-dress",
        name="Empire waist dress",
        description="Dress with a high waistline that elongates the torso.",
        body_shapes=[BodyShape.apple, BodyShape.rectangle, BodyShape.pear],
        colour_tags={
            Undertone.warm: ["Peach", "Gold", "Camel", "Rust"],
            Undertone.cool: ["Lavender", "Cool pink", "Navy", "Plum"],
            Undertone.neutral: ["Dusty rose", "Sage", "Mauve", "Navy"],
        },
        silhouette="Empire waist, flowy skirt",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20an%20empire%20waist%20dress%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="wide-leg-jumpsuit",
        name="Wide-leg jumpsuit",
        description="One-piece with wide legs and a defined or relaxed waist.",
        body_shapes=[BodyShape.inverted_triangle, BodyShape.rectangle, BodyShape.hourglass],
        colour_tags={
            Undertone.warm: ["Terracotta", "Olive", "Camel", "Warm brown"],
            Undertone.cool: ["Navy", "Charcoal", "Plum", "Teal"],
            Undertone.neutral: ["Charcoal", "Navy", "Taupe", "Dusty rose"],
        },
        silhouette="Wide legs, balanced proportions",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20a%20wide-leg%20jumpsuit%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="peplum-top",
        name="Peplum top + slim trousers",
        description="Peplum adds waist definition; pair with slim or straight trousers.",
        body_shapes=[BodyShape.rectangle, BodyShape.pear],
        colour_tags={
            Undertone.warm: ["Coral", "Cream", "Olive green", "Gold"],
            Undertone.cool: ["Cool pink", "Lavender", "Navy", "Mint"],
            Undertone.neutral: ["Blush", "Sage", "Mauve", "Charcoal"],
        },
        silhouette="Peplum waist, slim lower half",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20a%20peplum%20top%20and%20slim%20trousers%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="layered-outerwear",
        name="Layered look with belt",
        description="Layered top or dress with a belt to define the waist.",
        body_shapes=[BodyShape.rectangle, BodyShape.apple, BodyShape.hourglass],
        colour_tags={
            Undertone.warm: ["Camel", "Rust", "Olive", "Warm brown"],
            Undertone.cool: ["Navy", "Charcoal", "Dusty blue", "Plum"],
            Undertone.neutral: ["Taupe", "Navy", "Dusty rose", "Charcoal"],
        },
        silhouette="Layers with waist definition",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20woman%20wearing%20layered%20outerwear%20with%20a%20belt%20professional%20studio%20lighting%20white%20background"
    ),
]


OUTFIT_TEMPLATES_MALE: List[OutfitTemplate] = [
    OutfitTemplate(
        id="tee-overshirt-chinos",
        name="T-shirt + overshirt + chinos",
        description="Comfortable smart-casual layering with clean lines.",
        body_shapes=[BodyShape.rectangle, BodyShape.trapezoid, BodyShape.apple],
        colour_tags={
            Undertone.warm: ["Olive green", "Camel", "Cream", "Warm brown"],
            Undertone.cool: ["Navy", "Charcoal", "Slate blue", "Soft white"],
            Undertone.neutral: ["Taupe", "Navy", "Charcoal", "Soft white"],
        },
        silhouette="Layered top, straight chinos",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20man%20wearing%20a%20t-shirt%20overshirt%20and%20chinos%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="oxford-straight-jeans",
        name="Oxford shirt + straight-leg jeans",
        description="A classic combination that flatters most frames.",
        body_shapes=[BodyShape.rectangle, BodyShape.triangle, BodyShape.apple, BodyShape.trapezoid],
        colour_tags={
            Undertone.warm: ["Cream", "Camel", "Olive green", "Rust"],
            Undertone.cool: ["Soft white", "Navy", "Ice blue", "Charcoal"],
            Undertone.neutral: ["Soft white", "Navy", "Taupe", "Charcoal"],
        },
        silhouette="Clean shoulder line, straight legs",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20man%20wearing%20an%20oxford%20shirt%20and%20straight-leg%20jeans%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="polo-tapered-trousers",
        name="Polo + tapered trousers",
        description="Polished and breathable; great for warm days.",
        body_shapes=[BodyShape.trapezoid, BodyShape.rectangle, BodyShape.triangle],
        colour_tags={
            Undertone.warm: ["Olive green", "Camel", "Coral", "Cream"],
            Undertone.cool: ["Navy", "Mint", "Slate blue", "Cool pink"],
            Undertone.neutral: ["Sage", "Navy", "Mauve", "Soft white"],
        },
        silhouette="Structured collar, tapered leg",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20man%20wearing%20a%20polo%20shirt%20and%20tapered%20trousers%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="crewneck-bomber",
        name="Crewneck knit + bomber jacket",
        description="Adds structure and dimension without bulk.",
        body_shapes=[BodyShape.rectangle, BodyShape.apple, BodyShape.inverted_triangle],
        colour_tags={
            Undertone.warm: ["Camel", "Warm brown", "Olive", "Gold"],
            Undertone.cool: ["Charcoal", "Navy", "Plum", "Slate blue"],
            Undertone.neutral: ["Charcoal", "Taupe", "Navy", "Dusty rose"],
        },
        silhouette="Structured outerwear, straight fit",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20man%20wearing%20a%20crewneck%20knit%20and%20bomber%20jacket%20professional%20studio%20lighting%20white%20background"
    ),
    OutfitTemplate(
        id="open-collar-wide-leg",
        name="Open-collar shirt + straight/relaxed trousers",
        description="Balances a broader upper body with comfort-first lines.",
        body_shapes=[BodyShape.inverted_triangle, BodyShape.trapezoid],
        colour_tags={
            Undertone.warm: ["Cream", "Terracotta", "Olive", "Camel"],
            Undertone.cool: ["Soft white", "Navy", "Lavender", "Ice blue"],
            Undertone.neutral: ["Soft white", "Taupe", "Navy", "Sage"],
        },
        silhouette="Open collar, relaxed lower half",
        imageUrl="http://localhost:8000/generate_image?prompt=fashion%20photo%20of%20a%20man%20wearing%20an%20open-collar%20shirt%20and%20wide-leg%20trousers%20professional%20studio%20lighting%20white%20background"
    ),
]


def _get_silhouette_for_shape(shape: BodyShape, gender: Gender) -> SilhouetteRule | None:
    rules = SILHOUETTE_RULES_MALE if gender == Gender.male else SILHOUETTE_RULES_FEMALE
    for r in rules:
        if shape in r.body_shapes:
            return r
    return None


def _score_outfit(
    template: OutfitTemplate,
    body_shape: BodyShape,
    palette: ColourPalette,
    gender: Gender,
) -> tuple[float, str, str, List[str]]:
    shape_match = body_shape in template.body_shapes
    silhouette_rule = _get_silhouette_for_shape(body_shape, gender)

    primary_colours = template.colour_tags[palette.undertone]
    suggested_colours = [
        c for c in primary_colours if any(c.lower() in p.lower() for p in [*palette.primary, *palette.secondary])
    ]
    colour_match = bool(primary_colours)

    body_match = (
        f"Ideal for {body_shape.value}: {silhouette_rule.reasoning if silhouette_rule else 'Flatters your proportions.'}"
        if shape_match
        else f"Can work for {body_shape.value} with the right fit; consider {silhouette_rule.silhouette if silhouette_rule else 'balanced proportions'}."
    )

    score = 0.0
    score += 50 if shape_match else 20
    if colour_match:
        score += 30
    score += min(20, len(primary_colours) * 4)

    colour_match_text = (
        f"Colours from your palette: {', '.join(primary_colours[:4])}."
        if colour_match
        else f"Try these shades: {', '.join(primary_colours[:4])}."
    )

    return min(100.0, score), body_match, colour_match_text, primary_colours[:5]


def get_outfit_recommendations(body_shape: BodyShape, palette: ColourPalette, gender: Gender) -> list[OutfitSuggestion]:
    if gender == Gender.male:
        templates = OUTFIT_TEMPLATES_MALE
    elif gender == Gender.female:
        templates = OUTFIT_TEMPLATES_FEMALE
    else:
        templates = [*OUTFIT_TEMPLATES_FEMALE, *OUTFIT_TEMPLATES_MALE]

    results: list[OutfitSuggestion] = []

    for t in templates:
        score, body_match, colour_match, suggested_colours = _score_outfit(t, body_shape, palette, gender)
        silhouette_rule = _get_silhouette_for_shape(body_shape, gender)
        results.append(
            OutfitSuggestion(
                id=t.id,
                name=t.name,
                description=t.description,
                silhouette=t.silhouette,
                colours=suggested_colours,
                compatibilityScore=score,
                reasoning=f"{body_match} {colour_match}",
                bodyShapeMatch=silhouette_rule.reasoning if silhouette_rule else "Balanced silhouette.",
                colourMatch=f"Best in: {', '.join(suggested_colours)}.",
                imageUrl=t.imageUrl,
            )
        )

    results.sort(key=lambda o: o.compatibilityScore, reverse=True)
    return results

