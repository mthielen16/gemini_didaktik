from google import genai

# 1. Deinen API-Schlüssel hier einfügen (zwischen die Anführungszeichen!)
MEIN_API_KEY = "AIzaSyCPEstRMZs_dhAwGcaTkTntdLOreTK2zC0"

# 2. Verbindung zu Google herstellen
client = genai.Client(api_key=MEIN_API_KEY)

print("Sende Nachricht an die KI... Bitte warten.")

# 3. Die eigentliche Anfrage an das Modell
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Hallo! Ich bin ein Lehrer am Berufskolleg in NRW und baue gerade meine erste KI-App mit Python. Sag kurz Hallo und gib mir einen kurzen, motivierenden Satz!'
)

# 4. Die Antwort ausgeben
print("\n--- Antwort der KI ---")
print(response.text)
print("----------------------")