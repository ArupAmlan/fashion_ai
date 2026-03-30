from models import ColourPalette, Undertone


UNDERTONE_PALETTES = {
    Undertone.warm: {
        "primary": ["Cream", "Camel", "Terracotta", "Olive green", "Gold", "Rust", "Warm brown", "Peach", "Coral"],
        "secondary": ["Mustard", "Burgundy", "Forest green", "Bronze", "Amber"],
        "avoid": ["Cool grey", "Bright white", "Ice blue", "Silver", "Cool pink"],
    },
    Undertone.cool: {
        "primary": ["Navy", "Slate blue", "Silver grey", "Cool pink", "Mint", "Lavender", "Charcoal", "Ice blue", "Plum"],
        "secondary": ["Teal", "Rose", "Soft white", "Dusty blue", "Berry"],
        "avoid": ["Orange", "Yellow-gold", "Warm brown", "Camel", "Peach"],
    },
    Undertone.neutral: {
        "primary": ["Soft white", "Grey", "Dusty rose", "Sage", "Mauve", "Navy", "Olive", "Taupe", "Blush"],
        "secondary": ["Lavender", "Teal", "Camel", "Burgundy", "Charcoal"],
        "avoid": ["Bright orange", "Lime green", "Neon colours"],
    },
}

UNDERTONE_REASONING = {
    Undertone.warm: "Warm undertones are complemented by earthy, golden, and peachy tones. "
    "These colours bring out the natural warmth in your skin.",
    Undertone.cool: "Cool undertones look best in blues, pinks, and silvers. "
    "These hues harmonise with the subtle blue or pink in your complexion.",
    Undertone.neutral: "Neutral undertones can wear both warm and cool tones. "
    "Muted, balanced colours and soft neutrals flatter you most.",
}


def get_colour_palette_for_undertone(undertone: Undertone) -> ColourPalette:
    pal = UNDERTONE_PALETTES[undertone]
    return ColourPalette(
        undertone=undertone,
        primary=pal["primary"],
        secondary=pal["secondary"],
        avoid=pal["avoid"],
        reasoning=UNDERTONE_REASONING[undertone],
    )

