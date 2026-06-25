import time

from services.browser import create_browser, fetch_page
from services.logger import logger
from services.scraper import (
    check_if_are_new_apartments,
    get_recent_apartments,
    initialize_already_seen_file,
    update_most_recent_file,
)
from services.telegram import send_telegram_message

URLS = {
    "pillin_sur": {
        "chat_id": "-5514972809",
        "url": "https://www.portalinmobiliario.com/arriendo/departamento/3-dormitorios/_DisplayType_L_PriceRange_0CLP-1500000CLP_item*location_lat:-33.44005344441883*-33.408354691756145,lon:-70.61669981765749*-70.56430018234255?polygon_location=je~jE~y%7CmLiIc%5EoEqa%40w%40qQ%7DCkHuCmTv%40iCvE%7BDfGmAp%40eBhEqC%60GYhM%7DL%60GaCjDwFzJaG%3FhCfEvBvG%7CLtCvB~DlLfAfJi%40vMp%40fJnEbObDrSTjSjDnIkBIqBtAeDPkJlEyOz%40_RfFiXjDuClBUi%40",
    },
    "pillin_norte": {
        "chat_id": "-5514972809",
        "url": "https://www.portalinmobiliario.com/arriendo/departamento/3-dormitorios/_DisplayType_L_PriceRange_0CLP-1500000CLP_item*location_lat:-33.41385321995027*-33.38214490223779,lon:-70.61848481765746*-70.56608518234252?polygon_location=pw%7BjEre%7CmLiB%60%40mHX_Ch%40yDP%7DCh%40qIP_EgBeDOcDeAwGa%40iI_CqBoBy%40%3F%7BAs%40eHiG%7DA%7B%40sFmAq%40a%40uEkH%5D%7B%40%3Fi%40M%3FSs%40G%7B%40%5BY%5DyC%3F_F%7CE%7BGTq%40b%40Q%7CAoBv%40Gx%40cAlAeEp%40a%40rByCT%3FtAmAbBYxB%3FzAa%40fCQjBi%40jD_CbByB~%40i%40jDs%40%7CAGp%40a%40tAgBvGuEv%40QvE%3Fp%40WfA%3FzA%7CLrBnFlC%60DT%60Rj%40dEfIbPjBrKj%40%7CAb%40%7CDL%7CE%3FzKUH%7DAX",
    },
}


if __name__ == "__main__":
    initialize_already_seen_file(URLS)

    with create_browser() as page:
        while True:
            for key, commune in URLS.items():
                try:
                    page_source = fetch_page(page, commune["url"])
                except Exception as e:
                    logger.error(f"Failed to fetch {key}: {e}")
                    continue

                most_recent_apartments = get_recent_apartments(page_source, n_apartments=15)
                new_apartment_ids = check_if_are_new_apartments(key, most_recent_apartments)

                if len(new_apartment_ids) > 0:
                    logger.info(f"Found {len(new_apartment_ids)} new apartments in {key}")
                    new_apartments = {
                        id: most_recent_apartments[id]
                        for id in new_apartment_ids
                        if id in most_recent_apartments
                    }

                    for id, apartment in new_apartments.items():
                        logger.info(f"Sending message to Telegram for {apartment['title']}")
                        send_telegram_message(apartment["url"], commune["chat_id"])
                        time.sleep(0.05)

                    update_most_recent_file(key, new_apartments)
                else:
                    logger.info(f"No new apartments found for {key}. Skipping...")

            time.sleep(60 * 60 * 2)
