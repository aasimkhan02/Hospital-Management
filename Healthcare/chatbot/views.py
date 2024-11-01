from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import dialogflow_v2 as dialogflow
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def Dialogflow_webhook (request):
    body_unicode= request.body.decode('utf-8')
    body= json.loads(body_unicode)

    symptoms=body['queryresult']['parameter'].get("symptoms")

    if symptoms:
        if 'headache' in symptoms and 'fever' in symptoms:
            reply = "It looks like you might have the flu. Please rest and stay hydrated."
        elif 'chest pain' in symptoms and 'shortness of breath' in symptoms:
            reply = "These could be signs of something serious. Please seek immediate medical attention."
        else:
            reply = "I'm not sure what the exact issue is. Please consult a healthcare professional."

    else:
        reply = "I didn't understand your symptoms. Can you describe them again?"

    # Return the response back to Dialogflow
        return JsonResponse({"fulfillmentText": reply})