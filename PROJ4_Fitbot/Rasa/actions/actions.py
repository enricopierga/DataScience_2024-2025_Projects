from typing import Any, List, Text, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Form, SlotSet

from typing import Any, Text, Dict
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset, Restarted, UserUtteranceReverted

import logging
# Configurazione base del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActionStopBot(Action):
    def name(self) -> str:
        return "action_stop_bot"

    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Conversazione interrotta. Grazie per avermi usato! 👋"
        )
        return [AllSlotsReset(), Restarted()]

class ValidateFitnessForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fitness_form"

    async def validate_fitness_goal(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'fitness_goal' slot."""
        valid_goals = ["perdere peso", "aumentare la massa muscolare", "migliorare il tono fisico"]
        slot_value = slot_value.strip().lower()
        if slot_value in valid_goals:
            return {"fitness_goal": slot_value}
        dispatcher.utter_message(
            text=f"⚠️ L'obiettivo '{slot_value}' non è valido. Puoi scegliere tra: {', '.join(valid_goals)}. 🎯"
        )
        return {"fitness_goal": None}

    async def validate_experience_level(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'experience_level' slot."""
        valid_levels = ["principiante", "intermedio", "avanzato"]
        slot_value = slot_value.strip().lower()
        if slot_value in valid_levels:
            return {"experience_level": slot_value}
        dispatcher.utter_message(
            text=f"⚠️ Il livello '{slot_value}' non è valido. Puoi scegliere tra: {', '.join(valid_levels)}. 🏋️‍♂️"
        )
        return {"experience_level": None}

    async def validate_availability(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'availability' slot."""
        try:
            hours = int(slot_value)
            if 1 <= hours <= 168:
                return {"availability": hours}
        except ValueError:
            pass
        dispatcher.utter_message(
            text="⏰ Inserisci un numero valido di ore (1-168) per settimana! 🕒"
        )
        return {"availability": None}


class ActionSubmitFitnessForm(Action):
    def name(self) -> str:
        return "action_submit_fitness_form"

    def run(self, dispatcher, tracker, domain):
        fitness_goal = tracker.get_slot("fitness_goal")
        experience_level = tracker.get_slot("experience_level")
        availability = tracker.get_slot("availability")

        # Log dei dati raccolti
        logger.info(f"Obiettivo: {fitness_goal}, Livello: {experience_level}, Ore: {availability}")

        dispatcher.utter_message(
            text="🎉 Grazie! Ora conosco meglio i tuoi obiettivi. Procedo a creare il tuo piano personalizzato! 💪"
        )
        return [Form(None), SlotSet("requested_slot", None)]


class ActionCreatePersonalizedWorkout(Action):
    def name(self) -> str:
        return "action_create_personalized_workout"

    def run(self, dispatcher, tracker, domain):
        # Recupera i valori degli slot dal form
        fitness_goal = tracker.get_slot("fitness_goal")
        experience_level = tracker.get_slot("experience_level")
        availability = tracker.get_slot("availability")

        # Trasforma il valore di availability in un numero
        try:
            availability = int(availability)
        except (ValueError, TypeError):
            availability = 0  # Valore predefinito in caso di errore

        # Genera il piano in base ai valori raccolti
        workout_plan = self._generate_workout_plan(fitness_goal, experience_level, availability)

        # Messaggio di default se non è stato possibile generare un piano
        if not workout_plan:
            workout_plan = "❌ Non sono riuscito a generare un piano personalizzato. Per favore, fornisci maggiori dettagli sui tuoi obiettivi. 😊"

        # Invia il piano generato come messaggio al bot
        dispatcher.utter_message(
            text=f"📋 Ecco il tuo piano di allenamento personalizzato:\n{workout_plan} 🏋️‍♀️"
        )
        return []

    def _generate_workout_plan(self, fitness_goal, experience_level, availability):
        """
        Logica per generare un piano personalizzato in base agli slot raccolti.
        """
        if not fitness_goal or not experience_level or availability <= 0:
            return None

        # Piani per perdere peso
        if fitness_goal == "perdere peso":
            return self._generate_weight_loss_plan(experience_level, availability)

        # Piani per aumentare la massa muscolare
        elif fitness_goal == "aumentare la massa muscolare":
            return self._generate_muscle_gain_plan(experience_level, availability)

        # Piani per migliorare il tono fisico
        elif fitness_goal == "migliorare il tono fisico":
            return self._generate_tone_plan(experience_level, availability)

        return None

    def _generate_weight_loss_plan(self, experience_level, availability):
        """
        Genera un piano per perdere peso.
        """
        plans = {
            "principiante": f"⏳ Con {availability} ore disponibili, ti consiglio un programma di cardio leggero combinato con esercizi a corpo libero per principianti. 🏃‍♂️",
            "intermedio": f"🔥 Con {availability} ore disponibili, puoi seguire un programma di allenamento HIIT e cardio moderato con esercizi di resistenza. 🚴‍♀️",
            "avanzato": f"💪 Con {availability} ore disponibili, puoi seguire un programma avanzato di allenamenti combinati cardio e pesistica con alta intensità. 🏋️‍♂️"
        }
        return plans.get(experience_level)

    def _generate_muscle_gain_plan(self, experience_level, availability):
        """
        Genera un piano per aumentare la massa muscolare.
        """
        plans = {
            "principiante": f"🛠️ Con {availability} ore disponibili, inizia con esercizi base di pesistica per sviluppare la tecnica e costruire forza. 💪",
            "intermedio": f"🔩 Con {availability} ore disponibili, puoi seguire un programma di ipertrofia muscolare con focus su gruppi muscolari specifici. 🏋️‍♀️",
            "avanzato": f"🏆 Con {availability} ore disponibili, segui un programma avanzato con allenamenti giornalieri mirati a gruppi muscolari specifici. 🏋️‍♂️"
        }
        return plans.get(experience_level)

    def _generate_tone_plan(self, experience_level, availability):
        """
        Genera un piano per migliorare il tono fisico.
        """
        plans = {
            "principiante": f"🌱 Con {availability} ore disponibili, combina esercizi di resistenza leggeri con stretching e allenamenti a corpo libero. 🤸‍♂️",
            "intermedio": f"🌟 Con {availability} ore disponibili, puoi seguire un programma di tonificazione con pesi moderati e allenamenti funzionali. 🏋️‍♀️",
            "avanzato": f"💥 Con {availability} ore disponibili, segui un programma intenso di allenamenti funzionali e resistenza avanzata. 🔥"
        }
        return plans.get(experience_level)


class ActionAskMoreDetails(Action):
    def name(self) -> str:
        return "utter_ask_more_details"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="🔎 Vuoi sapere di più su esercizi specifici o consigli per il tuo piano? 💡"
        )
        return []


class ActionProvideExercises(Action):

    def name(self) -> str:
        return "action_provide_exercises"

    def run(self, dispatcher, tracker, domain):
        # Recupera le risposte dal form
        fitness_goal = tracker.get_slot("fitness_goal")
        experience_level = tracker.get_slot("experience_level")
        availability = tracker.get_slot("availability")

        # Converte i valori in lowercase per evitare case-sensitive
        if fitness_goal:
            fitness_goal = fitness_goal.lower()
        if experience_level:
            experience_level = experience_level.lower()

        # Trasforma il valore di availability in un numero
        try:
            availability = int(availability)
        except ValueError:
            availability = 0  # Default in caso di errore

        # Logica per generare esercizi
        if fitness_goal == "perdere peso":
            if experience_level == "principiante":
                exercises = """
                💪 Cardio leggero: Camminata veloce (20-30 minuti al giorno). Mantieni una velocità che ti permette di parlare ma non di cantare.
                🏋️‍♀️ Esercizi a corpo libero:
                  🔹 Squat (3 serie da 12-15 ripetizioni): Mantieni i talloni a terra e abbassati fino a quando le cosce sono parallele al pavimento.
                  🔹 Affondi (3 serie per gamba): Fai un passo avanti e abbassa il corpo fino a creare un angolo di 90 gradi con entrambe le gambe.
                  🔹 Mountain climbers (3 serie da 20 secondi): Porta le ginocchia al petto alternandole rapidamente.
                🌟 Consiglio: Focalizzati sulla costanza, non sull'intensità. Aumenta gradualmente la durata e aggiungi piccoli pesi alle caviglie per intensificare.
                """
            elif experience_level == "intermedio":
                exercises = """
                🏃‍♀️ Cardio moderato:
                  🔹 Corsa leggera o cyclette (30-40 minuti): Includi 1 minuto di corsa veloce ogni 5 minuti per aumentare la combustione calorica.
                🤸‍♀️ Esercizi combinati:
                  🔹 Burpees (3 serie da 12): Salta verso l'alto, scendi in posizione di plank e torna in piedi.
                  🔹 Plank dinamico (3 serie da 20 secondi): Alterna il sollevamento delle braccia durante il plank.
                  🔹 Squat con salto (3 serie da 12): Esegui un normale squat, ma aggiungi un salto esplosivo verso l'alto.
                🚀 Consiglio: Integra un allenamento HIIT (High Intensity Interval Training) di 20 minuti per massimizzare la perdita di peso.
                """
            elif experience_level == "avanzato":
                exercises = """
                🏋️‍♂️ Cardio intenso:
                  🔹 Interval training: 1 minuto di sprint seguito da 2 minuti di corsa lenta, ripetuto per 20-30 minuti.
                🏋️‍♀️ Esercizi di resistenza:
                  🔹 Deadlift (3 serie da 8): Solleva il bilanciere mantenendo la schiena dritta.
                  🔹 Kettlebell swings (3 serie da 15): Solleva il kettlebell con un movimento esplosivo dalle anche.
                  🔹 Push-up esplosivi (3 serie da 12): Salta con le mani dal pavimento in ogni ripetizione.
                💥 Consiglio: Combina pesistica e cardio in circuiti ad alta intensità, includendo poco tempo di recupero tra le serie.
                """
        
        elif fitness_goal == "aumentare la massa muscolare":
            if experience_level == "principiante":
                exercises = """
                🏋️‍♀️ Pesistica base:
                  🔹 Squat con manubri (3 serie da 10): Usa pesi leggeri per abituarti al movimento.
                  🔹 Panca piana con manubri (3 serie da 8-10): Solleva i manubri sopra il petto con controllo.
                  🔹 Rematore con bilanciere (3 serie da 8-10): Tieni la schiena dritta mentre tiri il bilanciere verso l'addome.
                🔧 Esercizi complementari:
                  🔹 Sollevamento laterale per le spalle (3 serie da 12): Usa manubri leggeri per allenare i deltoidi.
                  🔹 Curl per bicipiti (3 serie da 12): Solleva i manubri verso le spalle lentamente.
                🏆 Consiglio: Concentrati sulla tecnica e aumenta progressivamente il carico ogni 2 settimane.
                """
            elif experience_level == "intermedio":
                exercises = """
                🏋️‍♂️ Split routine:
                  🔹 Allenamenti alternati per petto/tricipiti, schiena/bicipiti, gambe/spalle.
                🔹 Bench press (3 serie da 6-8): Usa il bilanciere e mantieni i gomiti a 90 gradi.
                🔹 Squat profondo (3 serie da 10-12): Scendi il più possibile senza perdere la postura corretta.
                🔹 Deadlift (3 serie da 8): Mantieni il carico vicino al corpo durante il movimento.
                💪 Consiglio: Aumenta progressivamente il carico e integra superserie per intensità.
                """
            elif experience_level == "avanzato":
                exercises = """
                💥 Programma avanzato:
                  🔹 Allenamenti giornalieri mirati a gruppi muscolari specifici (es. push-pull-legs).
                🔹 Stacco da terra (4 serie da 5): Usa un peso elevato e lavora sulla forza.
                🔹 Military press (3 serie da 6-8): Solleva il bilanciere sopra la testa mantenendo una posizione stabile.
                🔹 Squat con bilanciere (3 serie da 6): Mantieni un peso pesante per lo sviluppo muscolare.
                🔹 Esercizi di isolamento: leg curl, pec deck per rifinire i dettagli muscolari.
                """
        
        elif fitness_goal == "migliorare il tono fisico":
            if experience_level == "principiante":
                exercises = """
                🏋️‍♀️ Resistenza leggera:
                  🔹 Elastici per glutei (3 serie da 15): Usa bande elastiche per resistenza.
                  🔹 Affondi laterali (3 serie da 12 per gamba): Alterna i lati per migliorare l'equilibrio.
                  🔹 Crunch (3 serie da 15): Solleva le spalle verso le ginocchia.
                🌟 **Stretching dinamico**:
                  🔹 Yoga leggero o Pilates: Dedica 20-30 minuti a sessioni leggere di stretching.
                """
            elif experience_level == "intermedio":
                exercises = """
                🤸‍♀️ Allenamento funzionale:
                  🔹 Kettlebell swing (3 serie da 15): Usa un movimento esplosivo per sollevare il kettlebell.
                  🔹 Push-up con variazioni (3 serie da 10-12): Alterna push-up classici e diamantati.
                  🔹 Squat con salto (3 serie da 12): Aggiungi esplosività ai movimenti.
                """
            elif experience_level == "avanzato":
                exercises = """
                🏋️‍♀️ Functional training avanzato:
                  🔹 TRX (3 serie da 12): Usa il TRX per esercizi come pull-up e squat.
                  🔹 Box jump (3 serie da 10): Salta su una scatola o un gradino alto.
                  🔹 Hollow hold (3 serie da 30 secondi): Mantieni la posizione in isometria.
                """
        
        else:
            exercises = "🤔 Non ho abbastanza informazioni per creare esercizi specifici. Prova a fornire dettagli più precisi sui tuoi obiettivi."

        # Invia gli esercizi al bot
        dispatcher.utter_message(text=f"🎉 **Ecco alcuni esercizi per te**:\n{exercises}")
        return []

class ActionGoodbye(Action):
    def name(self) -> str:
        return "utter_goodbye"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Grazie per avermi usato! A presto e buon allenamento!")
        return []
    
class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Mi dispiace, non ho capito la tua richiesta. Puoi riformularla o chiedermi qualcosa di diverso? 😊"
        )
        return []


class ActionResetSlots(Action):
    def name(self) -> str:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        # Reset di tutti gli slot utilizzati
        slots_to_reset = [
            "fitness_goal", 
            "experience_level", 
            "availability", 
            "diet_goal", 
            "food_preferences", 
            "calorie_intake"
        ]
        return [SlotSet(slot, None) for slot in slots_to_reset]

    
class ActionHandleFallback(Action):
    def name(self):
        return "action_handle_fallback"

    def run(self, dispatcher, tracker, domain):
        fallback_count = tracker.get_slot("fallback_count")
        
        # Incrementa il contatore di fallback
        if fallback_count is None:
            fallback_count = 0
        fallback_count += 1

        # Controlla il numero di fallback consecutivi
        if fallback_count >= 3:
            dispatcher.utter_message(
                text="Sembra che non riesca a capire la tua richiesta. 😓 Interrompo la conversazione. "
                     "Puoi sempre riprovare più tardi! 🙏"
            )
            # Resetta il contatore e termina la conversazione
            return [SlotSet("fallback_count", 0)]
        else:
            dispatcher.utter_message(
                text="Mi dispiace, non ho capito la tua richiesta. Puoi riformularla o chiedermi qualcosa di diverso? 😊"
            )
            return [SlotSet("fallback_count", fallback_count), UserUtteranceReverted()]
        
class ValidateDietForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_diet_form"

    async def validate_diet_goal(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'diet_goal' slot."""
        valid_goals = ["perdere peso", "aumentare massa", "mantenere il peso", "più energia"]
        normalized_value = slot_value.strip().lower()  # Normalize input
        if normalized_value in valid_goals:
            logger.info(f"Valid diet goal received: {normalized_value}")
            return {"diet_goal": normalized_value}
        dispatcher.utter_message(
            text=f"⚠️ L'obiettivo '{slot_value}' non è valido. Scegli tra: {', '.join(valid_goals)}."
        )
        return {"diet_goal": None}

    async def validate_calorie_intake(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'calorie_intake' slot."""
        try:
            calorie_intake = float(slot_value)  # Convert input to float
            if 1000 <= calorie_intake <= 5000:  # Check calorie range
                logger.info(f"Valid calorie intake received: {calorie_intake}")
                return {"calorie_intake": calorie_intake}
            dispatcher.utter_message(
                text="⚠️ Inserisci un valore tra 1000 e 5000 kcal per l'apporto calorico giornaliero."
            )
        except ValueError:
            dispatcher.utter_message(
                text="⚠️ Inserisci un valore numerico valido per l'apporto calorico!"
            )
        return {"calorie_intake": None}

    async def validate_food_preferences(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate the 'food_preferences' slot."""
        valid_preferences = ["vegano", "keto", "senza glutine", "no restrizioni"]
        normalized_value = slot_value.strip().lower()  # Normalize input
        if normalized_value in valid_preferences:
            logger.info(f"Valid food preference received: {normalized_value}")
            return {"food_preferences": normalized_value}
        dispatcher.utter_message(
            text=f"⚠️ La preferenza alimentare '{slot_value}' non è valida. Scegli tra: {', '.join(valid_preferences)}."
        )
        return {"food_preferences": None}




class ActionSubmitDietForm(Action):
    def name(self) -> Text:
        return "action_submit_diet_form"

    def run(self, dispatcher, tracker, domain):
        diet_goal = tracker.get_slot("diet_goal")
        food_preferences = tracker.get_slot("food_preferences")
        calorie_intake = tracker.get_slot("calorie_intake")

        dispatcher.utter_message(
            text=f"🎉 Grazie! Ecco il tuo piano personalizzato:\n"
                 f"- Obiettivo: {diet_goal}\n"
                 f"- Preferenze alimentari: {food_preferences}\n"
                 f"- Calorie giornaliere: {calorie_intake} kcal"
        )
        return []
    
class ActionProvideDietPlan(Action):
    def name(self) -> Text:
        return "action_provide_diet_plan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Recupera i valori degli slot
        diet_goal = tracker.get_slot("diet_goal")
        food_preferences = tracker.get_slot("food_preferences")
        calorie_intake = tracker.get_slot("calorie_intake")

         # Log per verificare i valori
        logger.info(f"Diet goal: {diet_goal}, Food preferences: {food_preferences}, Calorie intake: {calorie_intake}")
        
         # Controlla che tutti i valori siano presenti
        if not diet_goal or not food_preferences or not calorie_intake:
            dispatcher.utter_message(
                text="⚠️ Non è stato possibile generare un piano alimentare. Assicurati di fornire tutte le informazioni richieste."
            )
            return []
        
          # Normalizza i valori
        diet_goal = diet_goal.strip().lower()
        food_preferences = food_preferences.strip().lower()
        
        # Genera un piano alimentare in base agli slot
        diet_plan = self.generate_diet_plan(diet_goal, food_preferences, calorie_intake)

        # Invia il piano alimentare all'utente
        dispatcher.utter_message(text=f"🍽️ Ecco il tuo piano alimentare personalizzato:\n\n{diet_plan}")
        return []

    def generate_diet_plan(self, goal: str, preferences: str, calories: int) -> str:
        """
        Genera un piano alimentare personalizzato in base all'obiettivo, alle preferenze alimentari e all'apporto calorico.
        """
        # Distribuzione calorica in base ai pasti
        breakfast_calories = calories * 0.3
        lunch_calories = calories * 0.4
        dinner_calories = calories * 0.3

        # Piano alimentare per obiettivo e preferenze
        if goal == "perdere peso":
            if preferences == "vegano":
                return (
                    f"- 🥣 Colazione: Smoothie di spinaci, banana e latte di mandorla ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Insalata di quinoa con avocado, pomodori e tofu ({lunch_calories:.0f} kcal)\n"
                    f"- 🍲 Cena: Zuppa di verdure e ceci con crostini integrali ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "keto":
                return (
                    f"- 🍳 Colazione: Uova strapazzate con avocado e pancetta ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Insalata di pollo con olio d'oliva e noci ({lunch_calories:.0f} kcal)\n"
                    f"- 🐟 Cena: Salmone alla griglia con broccoli e burro ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "senza glutine":
                return (
                    f"- 🍞 Colazione: Pane senza glutine con burro di mandorle e marmellata ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Pollo alla griglia con riso integrale e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🐟 Cena: Trota al forno con patate dolci e asparagi ({dinner_calories:.0f} kcal)"
                )
            else:  # No restrizioni
                return (
                    f"- 🍎 Colazione: Yogurt greco con miele e frutta fresca ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Tacchino alla griglia con insalata di riso e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🐟 Cena: Filetto di pesce con verdure al vapore ({dinner_calories:.0f} kcal)"
                )

        elif goal == "aumentare massa":
            if preferences == "vegano":
                return (
                    f"- 🥑 Colazione: Porridge con latte di soia, semi di chia e frutta secca ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Burger di lenticchie con patate dolci e spinaci ({lunch_calories:.0f} kcal)\n"
                    f"- 🍛 Cena: Tofu marinato con riso basmati e zucchine grigliate ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "keto":
                return (
                    f"- 🍳 Colazione: Frittata di 4 uova con spinaci e formaggio ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥩 Pranzo: Bistecca con insalata di avocado e pomodori ({lunch_calories:.0f} kcal)\n"
                    f"- 🥓 Cena: Pollo al curry con crema di cocco e cavolfiore ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "senza glutine":
                return (
                    f"- 🍓 Colazione: Pancake senza glutine con sciroppo d'acero ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Pollo al forno con riso integrale e verdure grigliate ({lunch_calories:.0f} kcal)\n"
                    f"- 🥩 Cena: Bistecca di manzo con patate arrosto ({dinner_calories:.0f} kcal)"
                )
            else:  # No restrizioni
                return (
                    f"- 🍞 Colazione: Toast con burro d'arachidi e banana ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Pasta integrale con pollo e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🍛 Cena: Filetto di manzo con purè di patate e spinaci ({dinner_calories:.0f} kcal)"
                )

        elif goal == "più energia":
            if preferences == "vegano":
                return (
                    f"- 🌱 Colazione: Smoothie con latte di mandorla, banana, spinaci e semi di chia ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Couscous integrale con ceci e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🌮 Cena: Chili vegano con fagioli e mais ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "keto":
                return (
                    f"- 🍳 Colazione: Uova al tegamino con pancetta e spinaci ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Insalata di salmone affumicato e avocado ({lunch_calories:.0f} kcal)\n"
                    f"- 🍤 Cena: Gamberi saltati in burro con asparagi ({dinner_calories:.0f} kcal)"
                )
            elif preferences == "senza glutine":
                return (
                    f"- 🍞 Colazione: Pane senza glutine con marmellata e burro d'arachidi ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Insalata di riso con pollo e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🍣 Cena: Sushi senza glutine con pesce e avocado ({dinner_calories:.0f} kcal)"
                )
            else:  # No restrizioni
                return (
                    f"- 🍳 Colazione: Omelette con prosciutto e formaggio ({breakfast_calories:.0f} kcal)\n"
                    f"- 🥗 Pranzo: Insalata di tonno con patate lesse e verdure ({lunch_calories:.0f} kcal)\n"
                    f"- 🍛 Cena: Pollo arrosto con verdure al forno ({dinner_calories:.0f} kcal)"
                )

        # Default fallback plan
        return "⚠️ Non è stato possibile generare un piano alimentare. Per favore, verifica i dati inseriti."

