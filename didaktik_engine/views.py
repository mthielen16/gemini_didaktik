import os  # Neu hinzufügen
from django.shortcuts import render
from google import genai
from dotenv import load_dotenv  # Neu hinzufügen

# Lädt die Variablen aus der .env Datei
load_dotenv()

def ki_test_view(request):
    result = None
    if request.method == "POST":
        user_text = request.POST.get("user_input", "")
        if user_text:
            # Hol dir den Key aus der Umgebung
            api_key = os.getenv("GEMINI_API_KEY")
            
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Analysiere diesen Text didaktisch: {user_text}"
            )
            result = response.text

    return render(request, "didaktik_engine/index.html", {"result": result})