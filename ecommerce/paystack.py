import requests

class PayStack:
    PAYSTACK_SECRETE_KEY = "sk_test_29cef300b91ba8bdb76163d0f8693184ae81ca4d"
    base_url="https://api.paystack.co"

    def verify_payment(self,ref,*args,**kwargs):
