CATEGORY_LABELS = {
    "brand": "Brand",
    "gearbox": "Gearbox",
    "fuel_type": "Fuel type",
    "drive": "Drive",
    "voivodeship": "Voivodeship",
    "body_type": "Body",
    "color": "Color",
    "seller_type": "Seller type",
}

VALUE_LABELS = {
    "brand": {
        "Inny": "Other",
    },
    "gearbox": {
        "Automatyczna": "Automatic",
        "Manualna": "Manual",
    },
    "fuel_type": {
        "Benzyna": "Gasoline",
        "Benzyna+LPG": "Gasoline + LPG",
        "Diesel": "Diesel",
        "Hybryda": "Hybrid",
        "Hybryda Plug-in": "Plug-in hybrid",
    },
    "drive": {
        "4x4 (automatyczny)": "4x4 (on-demand)",
        "4x4 (ręczny)": "4x4 (part-time)",
        "4x4 (stały)": "4x4 (permanent)",
        "Na przednie koła": "Front-wheel drive",
        "Na tylne koła": "Rear-wheel drive",
    },
    "body_type": {
        "Auta małe": "Supermini",
        "Auta miejskie": "City car",
        "Coupe": "Coupe",
        "Kabriolet": "Convertible",
        "Kombi": "Estate",
        "Kompakt": "Hatchback",
        "Minivan": "MPV",
        "SUV": "SUV",
        "Sedan": "Sedan",
    },
    "color": {
        "Beżowy": "Beige",
        "Biały": "White",
        "Bordowy": "Maroon",
        "Brązowy": "Brown",
        "Błękitny": "Light blue",
        "Czarny": "Black",
        "Czerwony": "Red",
        "Fioletowy": "Purple",
        "Granatowy": "Navy",
        "Inny kolor": "Other color",
        "New Colour": "New color",
        "Niebieski": "Blue",
        "Pomarańczowy": "Orange",
        "Srebrny": "Silver",
        "Szary": "Gray",
        "Zielony": "Green",
        "Złoty": "Gold",
        "Żółty": "Yellow",
    },
    "voivodeship": {
        "dolnoslaskie": "Dolnoślaskie",
        "kujawsko-pomorskie": "Kujawsko-Pomorskie",
        "lodzkie": "Łódzkie",
        "lubelskie": "Lubelskie",
        "lubuskie": "Lubuskie",
        "malopolskie": "Małopolskie",
        "mazowieckie": "Mazowieckie",
        "opolskie": "Opolskie",
        "podkarpackie": "Podkarpackie",
        "podlaskie": "Podlaskie",
        "pomorskie": "Pomorskie",
        "slaskie": "Śląskie",
        "swietokrzyskie": "Świętokrzyskie",
        "warminsko-mazurskie": "Warmińsko-Mazurskie",
        "wielkopolskie": "Wielkopolskie",
        "zachodniopomorskie": "Zachodniopomorskie",
    },
    "seller_type": {
        "PRIVATE": "Private",
        "PROFESSIONAL": "Dealer / Company",
    },
}

FULLY_LABELED_FIELDS = frozenset({
    "gearbox",
    "fuel_type",
    "drive",
    "body_type",
    "color",
    "voivodeship",
    "seller_type",
})

EQUIPMENT_LABELS = {
    "leather_upholstery": "Leather upholstery",
    "dealership_serviced": "Serviced at a dealership",
    "panoramic_roof": "Panoramic roof",
    "led_headlights": "LED headlights",
    "led_taillights": "LED taillights",
    "first_owner": "One owner",
    "automatic_ac": "Automatic AC",
    "rearview_camera": "Rearview camera",
    "heated_seats": "Heated seats",
    "cruise_control": "Cruise control",
    "adaptive_cruise_control": "Adaptive cruise control",
    "traffic_sign_recognition": "Traffic sign assist",
    "wireless_charger": "Wireless charger",
    "android_auto": "Android Auto / CarPlay",
}

EQUIPMENT_PRESETS = [
    {"value": 15, "label": "Basic"},
    {"value": 38, "label": "Medium"},
    {"value": 60, "label": "High"},
    {"value": 90, "label": "Top"},
]


def untranslated_values(categories: dict[str, list[str]]) -> dict[str, list[str]]:
    missing = {}
    for field in FULLY_LABELED_FIELDS:
        known = VALUE_LABELS.get(field, {})
        unmapped = [value for value in categories.get(field, []) if value not in known]
        if unmapped:
            missing[field] = unmapped
    return missing
