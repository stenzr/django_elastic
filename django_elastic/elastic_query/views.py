from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import requests
import json


@api_view(["GET"])
def QueryCompute(request):
    url = "http://172.29.25.61:4444/datas/_search?size=0"
    headers = {
        'Content-Type': 'application/json'
    }
    if request.method == "GET":

        q = request.query_params.get("q", None)

        if q is not None:
            if q == 1:

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

                response = requests.request(
                    "GET", url, headers=headers, data=payload)

                return Response(response.text, status=status.HTTP_200_OK)

            elif q == 2:

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
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "GET", url, headers=headers, data=payload)

                return Response(response.text, status=status.HTTP_200_OK)
