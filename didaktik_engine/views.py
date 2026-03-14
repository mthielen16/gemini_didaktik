


import os
from django.shortcuts import render
from google import genai
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required

load_dotenv()
@login_required
def ki_test_view(request):
    # Session-Speicher für den Chat vorbereiten
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
    
    result = None
    display_history = request.session['chat_history']

    if request.method == 'POST':
        # Neustart-Knopf Logik
        if 'reset' in request.POST:
            request.session['chat_history'] = []
            request.session.modified = True
            return render(request, 'didaktik_engine/index.html', {'result': None, 'full_history': []})

        user_input = request.POST.get('user_input', '')
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        # Dein Experten-Prompt (ohne {user_text} am Ende!)
        system_instruction = """Du bist „Dobbi“, ein sachlicher, professionell-neutraler und streng kriteriengeleiteter didaktischer Gutachter für Lernsituationen an Berufskollegs. 
Deine Aufgabe ist die systematische, objektive und kritische Evaluation von Lernsituationen. Beziehe dich bei deiner Evaluation zwingend auf den Text, den der Nutzer eingibt.

### TONFALL UND STIL
- Sprache: Deutsch. Anrede: Sachliches „Sie“ oder professionelles „Du“.
- Stil: Objektiv, analytisch, akademisch und defizitorientiert (Qualitätsentwicklung).
- Verbotenes: Keine Emojis, keine Verspieltheit, keine beschönigenden Übertreibungen.

### FORMATIERUNG (Zwingend)
- Nutze AUSSCHLIESSLICH HTML-Tags (<h3>, <ul>, <li>, <strong>, <table>, <tr>, <th>, <td>).
- KEIN Markdown!
- Erstelle für jeden Schritt eine Tabelle: Prüfkriterium | Bewertung (0–2) | Begründung.

### WISSENSBASIS
1. DQR-Niveaus (besonders Niveau 4).
2. Handlungsorientierung (Aebli & AVIVA, vollständige Handlung).
3. Digitale Schlüsselkompetenzen (QUA-LIS NRW).
4. KI-Kompetenzen (3-N-Modell).

### PROZESSABLAUF
Führe eine vollständige Evaluation der Schritte 1 bis 4 durch (Einstiegsszenario, Handlungsprodukte, Kompetenzen, Ziele).
Berechne am Ende jeder Tabelle die Summe und verfasse einen nüchternen Fließtext zu den Mängeln.

### ABSCHLUSS (Nur am Ende)
- Kurzprofil der Lernsituation.
- Sequenzielle Gesamtübersicht (Tabelle der Punkte).
- Gesamtbewertung (kritisches Fazit).
- Priorisierte Überarbeitungsschritte (3-4 Punkte als <ol>).

Hier ist die zu evaluierende Lernsituation:"""

        try:
            # Chat mit Historie starten
            chat = client.chats.create(
                model="gemini-2.5-flash",
                config={'system_instruction': system_instruction},
                history=request.session['chat_history']
            )
            
            response = chat.send_message(user_input)
            result = response.text
            
            # Verlauf für Django "verdaubar" machen (JSON-kompatibel)
            updated_history = []
            for msg in chat.history:
                updated_history.append({
                    'role': msg.role, 
                    'parts': [{'text': msg.parts[0].text}]
                })
            
            request.session['chat_history'] = updated_history
            request.session.modified = True
            display_history = updated_history

        except Exception as e:
            result = f"<div class='alert alert-danger'>Fehler: {str(e)}</div>"

    return render(request, 'didaktik_engine/index.html', {
        'result': result, 
        'full_history': display_history
    })
