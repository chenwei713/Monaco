import requests
import time
import datetime
from email_utils import GmailClient
from data_utils import get_apt_data, rewrite_apt_data


def compose_email(apartments, all_apartments_list, new_apartments_list):
    message = "<h2 style='color:DodgerBlue;'>Apartments in BLVD $ < 3500</h2>"
    current_apartment_units = list(apartments.keys())
    for key in current_apartment_units:
        if key not in all_apartments_list:
            # Apartment removed
            message += "<strike>"
        message += ("<h4 style='color:red;'>" if key in new_apartments_list else "<h4>") + key + "</h4>"
        message += "<i>Bedroom: " + apartments[key]['bedroom'] + " Bathroom: " + apartments[key]['bathroom'] + "</i><br></br>"
        message += "<b style='color:green;'>" + "Price " + apartments[key]["price"][-1] + "</b><br></br>"
        message += "<b style='color:black;'>" + apartments[key]["building"] + "</b><br></br><br></br>"
        message += "<b>------------------------------</b>"

        if key not in all_apartments_list:
            message += "</strike>"
            del apartments[key]

    return message

def find_apartment():
    # URL of the webpage to scrape
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    url = "https://verisresidential.com/search-results/?beds_min=0&beds_max=1"

    url_ajax = "https://verisresidential.com/wp-admin/admin-ajax.php"

    # Send an HTTP GET request to the webpage

    apartments = get_apt_data()
    gmail_client = GmailClient()

    while True:
        try:
            response = requests.post(url_ajax, data={"action": "properties_query", "id": 1664}, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:

                new_apartment_list = []
                all_apartment_list = []
                for apt in response.json():
                    unit_number = apt['ra_unit_number']
                    building = apt['property_address'].split('.')[0]
                    price = apt['ra_rent']
                    bedroom = apt['ra_bedrooms']
                    bathroom = apt['ra_bathrooms']

                    if float(price) < 3500.0:
                        print(apt)
                        all_apartment_list.append(unit_number)
                        if unit_number not in apartments or (
                                apartments[unit_number]['price'][-1] != price):
                            if unit_number not in apartments:
                                apartments[unit_number] = {}
                            apartments[unit_number]['building'] = building
                            apartments[unit_number]['bedroom'] = bedroom
                            apartments[unit_number]['bathroom'] = bathroom
                            if 'price' not in apartments[unit_number]:
                                apartments[unit_number]['price'] = []
                            apartments[unit_number]['price'].append(price)

                            new_apartment_list.append(unit_number)

                if len(new_apartment_list) > 0 or len(apartments) > len(all_apartment_list):
                    gmail_client.send_email(compose_email(apartments, all_apartment_list, new_apartment_list))
                    print("Message sent " + str(datetime.datetime.now()))

                    rewrite_apt_data(apartments)
                    print("Apartments data updated in local file")

            else:
                print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        except Exception as e:
            print("error" + e)

        #
        # sleep 5 mins
        time.sleep(60 * 5)


if __name__ == "__main__":
  find_apartment()