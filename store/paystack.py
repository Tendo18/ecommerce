from django.conf import settings
import requests

class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"
    def verify_payment(self, ref, *args, **kwargs):
        path = f'transaction/verify/(ref)'
        headers = {
            "Authorization" : f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type" : "application/json",
        }
        url = self.base_url + path
        response=response.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('data'):
                return True, response_data['data'] #return status and data
            else:
                return False, response_data.get('message', 'verification failed')
        else:
            return False, response.json().get('message', 'Paymment verification failed')


