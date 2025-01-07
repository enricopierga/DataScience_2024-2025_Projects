from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class SubmitWorkoutForm(Action):
    def name(self) -> Text:
        return "action_submit_workout_form"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        goal = tracker.get_slot("goal")
        experience = tracker.get_slot("experience")
        availability = tracker.get_slot("availability")

        # Risposta al completamento della form
        dispatcher.utter_message(
            text=f"Grazie! Ti consiglierò un allenamento basato sul tuo obiettivo ({goal}), "
                 f"livello di esperienza ({experience}) e tempo disponibile ({availability})."
        )
        return []
