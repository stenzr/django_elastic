from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_protect

import requests
import json


@api_view(["GET"])
@csrf_protect
def QueryCompute(request):
    url = "http://172.29.25.61:4444/datas/_search?size=0"
    headers = {
        'Content-Type': 'application/json'
    }
    if request.method == "GET":

        q = request.GET.get("q", None)
        print(type(q))

        if q == str(1):

            payload = json.dumps({
                "aggs": {
                    "by_uid": {
                        "terms": {
                            "field": "uid"
                        },
                        "aggs": {
                            "total_sum": {
                                "sum": {
                                    "script": "doc['k1'].value + doc['k2'].value"
                                }
                            }
                        }
                    }
                }
            })
            print(payload)
            try:

                response = requests.request(
                    "GET", url, headers=headers, data=payload)
                print(response.text)

                return JsonResponse(response.json(), status=status.HTTP_200_OK, safe=False)
            except:
                return JsonResponse(json.dumps({'message': 'error'}), status=status.HTTP_404_NOT_FOUND, safe=False)

        elif q == str(2):

            payload = json.dumps({
                "aggs": {
                    "by_uid": {
                        "terms": {
                            "field": "uid"
                        },
                        "aggs": {
                            "k1_count": {
                                "cardinality": {
                                    "field": "k1"
                                }
                            },
                            "k2_count": {
                                "cardinality": {
                                    "field": "k2"
                                }
                            }
                        }
                    }
                }
            })

            try:
                response = requests.request(
                    "GET", url, headers=headers, data=payload)
                print(response.text)
                return JsonResponse(response.json(), status=status.HTTP_200_OK, safe=False)
            except:
                return JsonResponse(json.dumps({'message': 'error'}), status=status.HTTP_404_NOT_FOUND, safe=False)
