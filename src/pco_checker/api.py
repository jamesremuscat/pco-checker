import jsonapi_requests
import os

api = jsonapi_requests.Api.config({
    'API_ROOT': 'https://api.planningcenteronline.com/services/v2/',
    'AUTH': (os.environ['PCO_APPLICATION_ID'], os.environ['PCO_SECRET']),
    'TIMEOUT': 30
})
