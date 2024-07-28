import requests
import logging

LICENSES_GENERATE_AUTH_CODE = ''
LICENSES_OFFER_CODE = 1
LICENSES_GENERATE_URL = 'https://account.jetbrains.com/services/create-coupon'
LICENSES_GENERATE_TIMEOUT = 5000


def generate_license_code(days):
    if not LICENSES_GENERATE_AUTH_CODE:
        print('Auto generating licenses is_enabled, but auth parameters are not configured')
        return None

    payload = {'offer': LICENSES_OFFER_CODE, 'validityDays': days}
    headers = {'Authorization': LICENSES_GENERATE_AUTH_CODE}

    try:
        response = requests.post(LICENSES_GENERATE_URL, data=payload, headers=headers,
                                 timeout=LICENSES_GENERATE_TIMEOUT)
    except RequestException as e:
        print('Exception on generating license: %s', e)
        return None
    try:
        response_body = response.json()
    except ValueError:
        print('Failed to load json when generating license: %s', response.text)
        return None

    if not response_body:
        print('Wrong answer when generating license: %s', response.text)
        return None

    license_code = response_body.get('code')
    expire_date = response_body.get('validTill')
    if response.status_code != requests.codes.ok or not license_code or not expire_date:
        print('Failed to generate license: [%s] %s', response.status_code, response.text)
        return None

    try:
        expire_date = parse(expire_date).date()
    except (ValueError, TypeError):
        print('Failed to parse license expire date: %s', expire_date)
        return None

    return {
        'activation_code': license_code,
        'expire_date': expire_date
    }


generate_license_code(30)