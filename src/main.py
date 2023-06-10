from typing import Dict
from dotenv.main import load_dotenv
import os
import json
import openai
load_dotenv()

class PromptGenerator:
    def __init__(self, api_key: str):
        self.api_key = os.environ.get('CHATGPT_TOKEN', None)
        openai.api_key = self.api_key

    def generate_prompt(self, input_data: Dict) -> str:
        # Aquí puedes construir el prompt con base en la entrada. Por ejemplo:
        prompt = "Como un experto en pedagogía, analiza las siguientes sesiones de estudio.\n\n"

        input_data = json.loads(input_data)
        for session in input_data['sesiones']:
            prompt += f"Día: {session['día']}\n"
            for ronda in session['rondas']:
                prompt += f"\nDuración: {ronda['duracion']}\n"
                prompt += f"Objetivos: {', '.join(ronda['objetivos'])}\n"
                prompt += f"Resultado: {', '.join(ronda['resultado'])}\n"
                prompt += f"Acciones: {', '.join(ronda['acciones'])}\n"
                prompt += f"Puntuación de avance: {ronda['puntuacion_de_avance']}\n"
                prompt += f"Puntuación de satisfacción: {ronda['puntuacion_de_satisfaccion']}\n"
                prompt += f"Tiempo de descanso: {ronda['descanso'] if ronda['descanso'] else 'Ninguno'}\n"
            prompt += "\n\n"
            prompt += "Por favor, proporciona un análisis detallado de los siguientes aspectos:\n"
            prompt += "1. Hábitos de estudio: ¿Son consistentes las sesiones de estudio? ¿Son adecuadas las duraciones de estudio y descanso?\n"
            prompt += "2. Objetivos y resultados: ¿Los objetivos están claramente definidos? ¿Los resultados indican que se están logrando los objetivos?\n"
            prompt += "3. Bienestar emocional: ¿La puntuación de satisfacción sugiere un estado emocional saludable? ¿Hay algún indicio de estrés o agotamiento?\n"
            prompt += "4. Sugerencias para la mejora: ¿Cómo podrían mejorarse las sesiones de estudio para maximizar la eficacia y la satisfacción?\n"

        return prompt

    def request_chat_gpt(self, prompt: str, max_tokens: int = 4097,  temperature: float = 0.4) -> str:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt, max_tokens=max_tokens ,temperature=temperature)
        return response.choices[0].text.strip()

    def analyze_study_sessions(self, input_data: Dict) -> str:
        prompt = self.generate_prompt(input_data)
        analysis = self.request_chat_gpt(prompt)
        return analysis