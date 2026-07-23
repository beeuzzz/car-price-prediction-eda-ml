import json
import pandas as pd
from pathlib import Path

def android_auto(data):
    android = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "android_auto" in params:
                wartosc = "Tak"
        android.append(wartosc)
    return android


def swiatla_tylne_led(data):
    led_tyl = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "led_rear_lights" in params:
                wartosc = "Tak"
        led_tyl.append(wartosc)
    return led_tyl


def ladowarka_indukcyjna(data):
    ladowarka = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "wireless_device_charging" in params:
                wartosc = "Tak"
        ladowarka.append(wartosc)
    return ladowarka


def czytanie_znakow(data):
    znaki = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "traffic_sign_recognition" in params:
                wartosc = "Tak"
        znaki.append(wartosc)
    return znaki


def aktywny_tempomat(data):
    acc = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "distance_control" in params:
                wartosc = "Tak"
        acc.append(wartosc)
    return acc

def pierwszy_wlasciciel(data):
    wlasciciel = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "original_owner" in params:
                vals = params["original_owner"].get("values", [])
                if isinstance(vals, list) and len(vals) > 0:
                    if vals[0].get("label") == "Tak":
                        wartosc = "Tak"
        wlasciciel.append(wartosc)
    return wlasciciel


def klimatyzacja_automatyczna(data):
    klima = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "air_conditioning_type" in params:
                vals = params["air_conditioning_type"].get("values", [])
                if isinstance(vals, list) and len(vals) > 0:
                    etykieta = vals[0].get("label", "").lower()
                    # Wyłapujemy słowo "automatyczna" w wartości
                    if "automatyczna" in etykieta:
                        wartosc = "Tak"
        klima.append(wartosc)
    return klima


def kamera_cofania(data):
    kamera = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "rear_view_camera" in params:
                wartosc = "Tak"
        kamera.append(wartosc)
    return kamera


def podgrzewane_fotele(data):
    fotele = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            # Sprawdzamy fotel kierowcy jako reprezentatywny
            if isinstance(params, dict) and "heated_seat_driver" in params:
                wartosc = "Tak"
        fotele.append(wartosc)
    return fotele


def tempomat(data):
    tempomat_lst = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "cruisecontrol_type" in params:
                wartosc = "Tak"
        tempomat_lst.append(wartosc)
    return tempomat_lst

def serwis_aso(data):
    aso = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict):
                service = params.get("service_record", {})
                if isinstance(service, dict):
                    vals = service.get("values", [])
                    if isinstance(vals, list) and len(vals) > 0:
                        if vals[0].get("label") == "Tak":
                            wartosc = "Tak"
        aso.append(wartosc)
    return aso


def pochodzenie_polska(data):
    pochodzenie = []
    for ogloszenie in data:
        wartosc = "Polska" 
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict):
                
                # Najpierw sprawdzamy konkretny kraj (żeby wyłapać USA)
                kraj = params.get("country_origin", {})
                if isinstance(kraj, dict) and kraj.get("values"):
                    vals = kraj.get("values", [])
                    if isinstance(vals, list) and len(vals) > 0:
                        etykieta = vals[0].get("label", "").lower()
                        kod = vals[0].get("value", "").lower()
                        
                        if kod == "usa" or "stany zjednoczone" in etykieta:
                            wartosc = "USA"
                        else:
                            wartosc = "Importowany"
                
                # Jeśli brak podanego kraju, ale ma ogólną flagę "Importowany"
                elif "is_imported_car" in params:
                    importowane = params.get("is_imported_car", {})
                    if isinstance(importowane, dict) and importowane.get("values"):
                        vals = importowane.get("values", [])
                        if isinstance(vals, list) and len(vals) > 0:
                            if vals[0].get("label") == "Tak":
                                wartosc = "Importowany"
                                
        pochodzenie.append(wartosc)
    return pochodzenie


def tapicerka_skorzana(data):
    skora = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            # Sprawdzamy, czy w słowniku w ogóle występuje klucz tapicerki
            if isinstance(params, dict) and "upholstery_type" in params:
                wartosc = "Tak"
        skora.append(wartosc)
    return skora

def dach_panoramiczny(data):
    dach = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "sunroof" in params:
                wartosc = "Tak"
        dach.append(wartosc)
    return dach


def swiatla_led(data):
    led = []
    for ogloszenie in data:
        wartosc = "Nie"
        if isinstance(ogloszenie, dict):
            params = ogloszenie.get("parametersDict", {})
            if isinstance(params, dict) and "led_daytime_running_lights" in params:
                wartosc = "Tak"
        led.append(wartosc)
    return led


def ilosc_wyposazenia(data):
    wyposazenie_count = []
    for ogloszenie in data:
        liczba = 0
        if isinstance(ogloszenie, dict):
            equipment_list = ogloszenie.get("equipment")
            # Sprawdzenie, czy klucz istnieje i jest listą
            if isinstance(equipment_list, list):
                for kategoria in equipment_list:
                    if isinstance(kategoria, dict):
                        values = kategoria.get("values")
                        # Dodajemy długość tylko, jeśli values jest faktycznie listą
                        if isinstance(values, list):
                            liczba += len(values)
        
        wyposazenie_count.append(liczba)
    return wyposazenie_count


def liczba_drzwi(data):
    drzwi = []
    for ogloszenie in data:
        wartosc = None
        if isinstance(ogloszenie, dict):
            details = ogloszenie.get("details")
            if isinstance(details, list):
                for detail in details:
                    # Upewniamy się, że detail to słownik przed wywołaniem .get()
                    if isinstance(detail, dict) and detail.get("key") == "door_count":
                        wartosc = detail.get("value")
                        break
        
        drzwi.append(wartosc)
    return drzwi


def typ_sprzedawcy(data):
    typ = []
    for ogloszenie in data:
        wartosc = None
        if isinstance(ogloszenie, dict):
            seller_info = ogloszenie.get("seller")
            if isinstance(seller_info, dict):
                wartosc = seller_info.get("type")
                
        typ.append(wartosc)
    return typ

def moc_silnika(data):
    mocSilnika = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "engine_power":
                mocSilnika.append(detail.get("value", None))
                break
        else:
            mocSilnika.append(None)
    return mocSilnika


def skrzynia_biegow(data):
    skrzyniaBiegow = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "gearbox":
                skrzyniaBiegow.append(detail.get("value", None))
                break
        else:
            skrzyniaBiegow.append(None)
    return skrzyniaBiegow


def napęd(data):
    napęd = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "transmission":
                napęd.append(detail.get("value", None))
                break
        else:
            napęd.append(None)
    return napęd


def marka(data):
    marki = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "make":
                marki.append(detail.get("value", None))
                break
        else:
            marki.append(None)
    return marki


def model(data):
    modele = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "model":
                modele.append(detail.get("value", None))
                break
        else:
            modele.append(None)
    return modele


def cena(data):
    ceny = []
    for ogloszenie in data:
        price_info = ogloszenie.get("priceList", {})
        if price_info.get("currency") is not None and price_info.get("value") is not None:
            ceny.append(price_info.get("value", None) + " " +
                        price_info.get("currency", None))
        else:
            ceny.append(None)

    return ceny


def paliwo(data):
    paliwo = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "fuel_type":
                paliwo.append(detail.get("value", None))
                break
        else:
            paliwo.append(None)
    return paliwo


def wojewodztwo(data):
    wojewodztwo = []
    for ogloszenie in data:
        wojewodztwo.append(
            ogloszenie["seller"]["location"]["canonicals"].get("region", None))
    return wojewodztwo


def nadwozie(data):
    nadwozie = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "body_type":
                nadwozie.append(detail.get("value", None))
                break
        else:
            nadwozie.append(None)
    return nadwozie


def kolor(data):
    kolor = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "color":
                kolor.append(detail.get("value", None))
                break
        else:
            kolor.append(None)
    return kolor


def rok_produkcji(data):
    rokProdukcji = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "year":
                rokProdukcji.append(detail.get("value", None))
                break
        else:
            rokProdukcji.append(None)
    return rokProdukcji


def przebieg(data):
    przebieg = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "mileage":
                przebieg.append(detail.get("value", None))
                break
        else:
            przebieg.append(None)
    return przebieg


def pojemnosc_silnika(data):
    pojemnoscSilnika = []
    for ogloszenie in data:
        details = ogloszenie.get("details", [])
        for detail in details:
            if detail.get("key") == "engine_capacity":
                pojemnoscSilnika.append(detail.get("value", None))
                break
        else:
            pojemnoscSilnika.append(None)
    return pojemnoscSilnika


def czy_uszkodzony(data):
    czyUszkodzony = []
    for ogloszenie in data:
        parameters = ogloszenie.get("parametersDict", {})
        damaged = parameters.get("damaged", {}).get("values", [])
        bezwypadkowy = parameters.get("no_accident", {}).get("values", [])
        if damaged:
            czyUszkodzony.append(damaged[0].get("label"))
        else:
            if bezwypadkowy and bezwypadkowy[0].get("label") == "Tak":
                czyUszkodzony.append("Nie")
            else:
                czyUszkodzony.append(None)

    return czyUszkodzony


def stworz_dataframe(data):
    dane = {

        "cena": cena(data),

        "marka": marka(data),

        "rok_produkcji": rok_produkcji(data),

        "pojemnosc_silnika": pojemnosc_silnika(data),

        "przebieg": przebieg(data),

        "moc_silnika": moc_silnika(data),

        "skrzynia_biegow": skrzynia_biegow(data),

        "paliwo": paliwo(data),

        "naped": napęd(data),

        "wojewodztwo": wojewodztwo(data),

        "nadwozie": nadwozie(data),

        "kolor": kolor(data),

        "uszkodzony": czy_uszkodzony(data),

        "ilosc_wyposazenia": ilosc_wyposazenia(data),

        "liczba_drzwi": liczba_drzwi(data),

        "typ_sprzedawcy": typ_sprzedawcy(data),

        "skorzana_tapicerka": tapicerka_skorzana(data),

        "importowany": pochodzenie_polska(data),

        "serwis_aso": serwis_aso(data),

        "dach_panoramiczny": dach_panoramiczny(data),

        "swiatla_led": swiatla_led(data),

        "pierwszy_wlasciciel": pierwszy_wlasciciel(data),

        "klimatyzacja_automatyczna": klimatyzacja_automatyczna(data),

        "kamera_cofania": kamera_cofania(data),

        "podgrzewane_fotele": podgrzewane_fotele(data),

        "tempomat": tempomat(data),

        'aktywny_tempomat': aktywny_tempomat(data),

        'czytanie_znakow': czytanie_znakow(data),

        'ladowarka_indukcyjna': ladowarka_indukcyjna(data),

        'swiatla_tylne_led': swiatla_tylne_led(data),

        'android_auto': android_auto(data),

        

    }

    df = pd.DataFrame(dane)
    return df


def main():
    data_folder = Path("data/dane_samochody")

    list_of_files = [
        'merged_data.json'
        ]
    
    df = pd.DataFrame()

    for file_name in list_of_files:
        path = data_folder / file_name

        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        df_c = stworz_dataframe(data)

        df = pd.concat([df, df_c], ignore_index=True)
    save_path = Path("data/dane_ogloszen_po_ekstrakcji.csv")
    df.to_csv(save_path, index=False)


if __name__ == "__main__":
    main()
