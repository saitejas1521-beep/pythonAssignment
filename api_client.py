import requests
import logging

class ZipApiClient:
    def __init__(self, config=None):
        api_config = config.get("api", {}) if config else {}
        self.base_url = api_config.get("base_url", "http://api.zippopotam.us/us/{}")
        self.timeout = api_config.get("timeout_seconds", 5)

    def get_state_for_zip(self, zip_code):
        try:
            url = self.base_url.format(zip_code)
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if "places" in data and len(data["places"]) > 0:
                # Get the state and state abbreviation
                state = data["places"][0]["state"]
                state_abbr = data["places"][0]["state abbreviation"]
                return f"{state} ({state_abbr})"
            return "Unknown State"
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return "Invalid Zip Code"
            logging.error(f"HTTP error occurred while fetching zip {zip_code}: {e}")
            return "Error Processing"
        except Exception as e:
            logging.error(f"Error fetching zip {zip_code}: {e}")
            return "Error Processing"
