from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random

class ActionSuggestWorkout(Action):
    def name(self):
        return "action_suggest_workout"

    def run(self, dispatcher, tracker, domain):
        workouts = [
            "30 minuti di cardio moderato",
            "3 serie di squat, 10 ripetizioni ciascuna",
            "Allenamento HIIT di 20 minuti",
            "Sessione di yoga rilassante di 15 minuti"
        ]
        workout = random.choice(workouts)
        dispatcher.utter_message(text=f"Ti consiglio: {workout}")
        return []

class ActionSuggestMeal(Action):
    def name(self):
        return "action_suggest_meal"

    def run(self, dispatcher, tracker, domain):
        meals = [
            "Un frullato proteico con banana e spinaci",
            "Pollo alla griglia con verdure cotte",
            "Insalata con tonno e avocado",
            "Porridge d'avena con frutta fresca"
        ]
        meal = random.choice(meals)
        dispatcher.utter_message(text=f"Ti consiglio: {meal}")
        return []

class ActionEsercizio(Action):
    def name(self) -> Text:
        return "action_richiesta_esercizio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        esercizio = "curl"  # Esempio, dovresti implementare la logica per scegliere l'esercizio
        if esercizio == "curl":
            dispatcher.utter_message(text="Ecco un esercizio per le braccia: prova i curl con i manubri.")
            dispatcher.utter_message(text="I curl con i manubri sono un ottimo esercizio per sviluppare i bicipiti.")
            dispatcher.utter_message(image="images/link_immagine_curl.jpg")  # Percorso relativo all'immagine
        
        # Aggiungi altre condizioni per altri esercizi
        return []
