import json
import pandas as pd
from pathlib import Path

def extract_android_auto(listings):
    android_auto_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "android_auto" in params:
                extracted_value = "Tak"
        android_auto_values.append(extracted_value)
    return android_auto_values


def extract_led_rear_lights(listings):
    led_rear_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "led_rear_lights" in params:
                extracted_value = "Tak"
        led_rear_values.append(extracted_value)
    return led_rear_values


def extract_wireless_charging(listings):
    wireless_charging_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "wireless_device_charging" in params:
                extracted_value = "Tak"
        wireless_charging_values.append(extracted_value)
    return wireless_charging_values


def extract_traffic_sign_recognition(listings):
    traffic_sign_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "traffic_sign_recognition" in params:
                extracted_value = "Tak"
        traffic_sign_values.append(extracted_value)
    return traffic_sign_values


def extract_adaptive_cruise_control(listings):
    adaptive_cruise_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "distance_control" in params:
                extracted_value = "Tak"
        adaptive_cruise_values.append(extracted_value)
    return adaptive_cruise_values

def extract_original_owner(listings):
    original_owner_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "original_owner" in params:
                values = params["original_owner"].get("values", [])
                if isinstance(values, list) and len(values) > 0:
                    if values[0].get("label") == "Tak":
                        extracted_value = "Tak"
        original_owner_values.append(extracted_value)
    return original_owner_values


def extract_automatic_air_conditioning(listings):
    automatic_air_conditioning_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "air_conditioning_type" in params:
                values = params["air_conditioning_type"].get("values", [])
                if isinstance(values, list) and len(values) > 0:
                    label = values[0].get("label", "").lower()
                    if "automatyczna" in label:
                        extracted_value = "Tak"
        automatic_air_conditioning_values.append(extracted_value)
    return automatic_air_conditioning_values


def extract_rear_view_camera(listings):
    rear_view_camera_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "rear_view_camera" in params:
                extracted_value = "Tak"
        rear_view_camera_values.append(extracted_value)
    return rear_view_camera_values


def extract_heated_seats(listings):
    heated_seats_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "heated_seat_driver" in params:
                extracted_value = "Tak"
        heated_seats_values.append(extracted_value)
    return heated_seats_values


def extract_cruise_control(listings):
    cruise_control_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "cruisecontrol_type" in params:
                extracted_value = "Tak"
        cruise_control_values.append(extracted_value)
    return cruise_control_values

def extract_authorized_service_history(listings):
    authorized_service_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict):
                service = params.get("service_record", {})
                if isinstance(service, dict):
                    values = service.get("values", [])
                    if isinstance(values, list) and len(values) > 0:
                        if values[0].get("label") == "Tak":
                            extracted_value = "Tak"
        authorized_service_values.append(extracted_value)
    return authorized_service_values


def extract_origin_country(listings):
    origin_country_values = []
    for listing in listings:
        extracted_value = "Polska"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict):

                country = params.get("country_origin", {})
                if isinstance(country, dict) and country.get("values"):
                    values = country.get("values", [])
                    if isinstance(values, list) and len(values) > 0:
                        label = values[0].get("label", "").lower()
                        code = values[0].get("value", "").lower()

                        if code == "usa" or "stany zjednoczone" in label:
                            extracted_value = "USA"
                        else:
                            extracted_value = "Importowany"

                elif "is_imported_car" in params:
                    imported = params.get("is_imported_car", {})
                    if isinstance(imported, dict) and imported.get("values"):
                        values = imported.get("values", [])
                        if isinstance(values, list) and len(values) > 0:
                            if values[0].get("label") == "Tak":
                                extracted_value = "Importowany"

        origin_country_values.append(extracted_value)
    return origin_country_values


def extract_leather_upholstery(listings):
    leather_upholstery_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "upholstery_type" in params:
                extracted_value = "Tak"
        leather_upholstery_values.append(extracted_value)
    return leather_upholstery_values

def extract_panoramic_roof(listings):
    panoramic_roof_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "sunroof" in params:
                extracted_value = "Tak"
        panoramic_roof_values.append(extracted_value)
    return panoramic_roof_values


def extract_led_daytime_lights(listings):
    led_daytime_values = []
    for listing in listings:
        extracted_value = "Nie"
        if isinstance(listing, dict):
            params = listing.get("parametersDict", {})
            if isinstance(params, dict) and "led_daytime_running_lights" in params:
                extracted_value = "Tak"
        led_daytime_values.append(extracted_value)
    return led_daytime_values


def extract_equipment_count(listings):
    equipment_count_values = []
    for listing in listings:
        count = 0
        if isinstance(listing, dict):
            equipment_list = listing.get("equipment")
            if isinstance(equipment_list, list):
                for category in equipment_list:
                    if isinstance(category, dict):
                        values = category.get("values")
                        if isinstance(values, list):
                            count += len(values)

        equipment_count_values.append(count)
    return equipment_count_values


def extract_seller_type(listings):
    seller_type_values = []
    for listing in listings:
        extracted_value = None
        if isinstance(listing, dict):
            seller_info = listing.get("seller")
            if isinstance(seller_info, dict):
                extracted_value = seller_info.get("type")

        seller_type_values.append(extracted_value)
    return seller_type_values

def extract_engine_power(listings):
    engine_power_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "engine_power":
                engine_power_values.append(detail.get("value", None))
                break
        else:
            engine_power_values.append(None)
    return engine_power_values


def extract_gearbox_type(listings):
    gearbox_type_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "gearbox":
                gearbox_type_values.append(detail.get("value", None))
                break
        else:
            gearbox_type_values.append(None)
    return gearbox_type_values


def extract_drivetrain(listings):
    drivetrain_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "transmission":
                drivetrain_values.append(detail.get("value", None))
                break
        else:
            drivetrain_values.append(None)
    return drivetrain_values


def extract_brand(listings):
    brand_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "make":
                brand_values.append(detail.get("value", None))
                break
        else:
            brand_values.append(None)
    return brand_values


def extract_model(listings):
    model_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "model":
                model_values.append(detail.get("value", None))
                break
        else:
            model_values.append(None)
    return model_values


def extract_price(listings):
    price_values = []
    for listing in listings:
        price_info = listing.get("priceList", {})
        if price_info.get("currency") is not None and price_info.get("value") is not None:
            price_values.append(price_info.get("value", None) + " " +
                        price_info.get("currency", None))
        else:
            price_values.append(None)

    return price_values


def extract_fuel_type(listings):
    fuel_type_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "fuel_type":
                fuel_type_values.append(detail.get("value", None))
                break
        else:
            fuel_type_values.append(None)
    return fuel_type_values


def extract_region(listings):
    region_values = []
    for listing in listings:
        region_values.append(
            listing["seller"]["location"]["canonicals"].get("region", None))
    return region_values


def extract_body_type(listings):
    body_type_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "body_type":
                body_type_values.append(detail.get("value", None))
                break
        else:
            body_type_values.append(None)
    return body_type_values


def extract_color(listings):
    color_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "color":
                color_values.append(detail.get("value", None))
                break
        else:
            color_values.append(None)
    return color_values


def extract_production_year(listings):
    production_year_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "year":
                production_year_values.append(detail.get("value", None))
                break
        else:
            production_year_values.append(None)
    return production_year_values


def extract_mileage(listings):
    mileage_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "mileage":
                mileage_values.append(detail.get("value", None))
                break
        else:
            mileage_values.append(None)
    return mileage_values


def extract_engine_capacity(listings):
    engine_capacity_values = []
    for listing in listings:
        details = listing.get("details", [])
        for detail in details:
            if detail.get("key") == "engine_capacity":
                engine_capacity_values.append(detail.get("value", None))
                break
        else:
            engine_capacity_values.append(None)
    return engine_capacity_values


def extract_damage_status(listings):
    damage_status_values = []
    for listing in listings:
        parameters = listing.get("parametersDict", {})
        damaged = parameters.get("damaged", {}).get("values", [])
        accident_free = parameters.get("no_accident", {}).get("values", [])
        if damaged:
            damage_status_values.append(damaged[0].get("label"))
        else:
            if accident_free and accident_free[0].get("label") == "Tak":
                damage_status_values.append("Nie")
            else:
                damage_status_values.append(None)

    return damage_status_values


def build_dataframe(listings):
    columns = {

        "cena": extract_price(listings),

        "marka": extract_brand(listings),

        "rok_produkcji": extract_production_year(listings),

        "pojemnosc_silnika": extract_engine_capacity(listings),

        "przebieg": extract_mileage(listings),

        "moc_silnika": extract_engine_power(listings),

        "skrzynia_biegow": extract_gearbox_type(listings),

        "paliwo": extract_fuel_type(listings),

        "naped": extract_drivetrain(listings),

        "wojewodztwo": extract_region(listings),

        "nadwozie": extract_body_type(listings),

        "kolor": extract_color(listings),

        "uszkodzony": extract_damage_status(listings),

        "ilosc_wyposazenia": extract_equipment_count(listings),

        "typ_sprzedawcy": extract_seller_type(listings),

        "skorzana_tapicerka": extract_leather_upholstery(listings),

        "importowany": extract_origin_country(listings),

        "serwis_aso": extract_authorized_service_history(listings),

        "dach_panoramiczny": extract_panoramic_roof(listings),

        "swiatla_led": extract_led_daytime_lights(listings),

        "pierwszy_wlasciciel": extract_original_owner(listings),

        "klimatyzacja_automatyczna": extract_automatic_air_conditioning(listings),

        "kamera_cofania": extract_rear_view_camera(listings),

        "podgrzewane_fotele": extract_heated_seats(listings),

        "tempomat": extract_cruise_control(listings),

        'aktywny_tempomat': extract_adaptive_cruise_control(listings),

        'czytanie_znakow': extract_traffic_sign_recognition(listings),

        'ladowarka_indukcyjna': extract_wireless_charging(listings),

        'swiatla_tylne_led': extract_led_rear_lights(listings),

        'android_auto': extract_android_auto(listings),



    }

    dataframe = pd.DataFrame(columns)
    return dataframe


def main():
    data_folder = Path("data/car_data")

    file_names = [
        'merged_data.json'
        ]

    combined_dataframe = pd.DataFrame()

    for file_name in file_names:
        path = data_folder / file_name

        with open(path, 'r', encoding='utf-8') as file:
            listings = json.load(file)

        file_dataframe = build_dataframe(listings)

        combined_dataframe = pd.concat([combined_dataframe, file_dataframe], ignore_index=True)
    save_path = Path("data/extracted_listings.csv")
    combined_dataframe.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
