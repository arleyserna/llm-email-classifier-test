from openai import OpenAI
import logging
import os



class LLMService:

    """
    This class handles all related to the LLM API interations.

    """

    def __init__(self, api_key: str):

        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logging.basicConfig(filename='email_classifier.log', encoding='utf-8', level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def classify(self, email: dict, valid_categories: list[str]) -> dict:
        
        response = None  # Initialize response variable

        try:
            # Construct the prompt for classification
            prompt = f"Classify the following email into one of these categories: {', '.join(valid_categories)}.\n\nEmail:\nSubject: {email['subject']}\nBody: {email['body']}"
            
            # Call the OpenAI API for classification
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a customer service assistant. Your task is to read emails and classify each one into one of the following categories based on its subject and body: complaint, inquiry, feedback, support_request, or other.\
                      You must return only the category name, in lowercase, with no punctuation or explanation. Return nothing else."
            },
                     {"role": "user", "content": prompt}
                    ],
                temperature=0.5,
                max_tokens=10,
                top_p=1,
            )
            
            # Extract and validate the classification
            classification = response.choices[0].message.content.strip().lower()

            if classification in valid_categories:
                return {"category":classification}
            
        except Exception as e:

            self.logger.error(f"Error during email classification: {e}")
            return {"category":None}

    def generate_response(self, classification: str, email: dict) -> dict:

        try:
            # Prompt to for the response email.
            prompt =  f"Write a formal response to the following email. It has been categorized as '{classification}'. \
                      The response must be short not, more than 200 tokens and must be polite and indicate that the issue has been transferred to the corresponding department and will be solved ASAP.\n\n\
                      Email:\nSubject: {email['subject']}\nBody: {email['body']}"

            print(f"It was no possible to process this request")

            # Call the OpenAI API for classification
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a customer service assistant. Your task is to respond the sender email, based upon the classification. you must be polite, respectfull and service focused, \
                     also you must indicate that you are the Company AI Customer Agent."},
                    {"role": "user", "content": prompt}
                    ],
                temperature=0.5,
                max_tokens=3000,
                top_p=1,
            )

            reply = response.choices[0].message.content.strip()

            return reply

            #return {"response": reply}

        except Exception as e:
            
            self.logger.error(f"Error while generating the response {e}")
            return None

        # Validar el tipo de salida que sea JSON, para luego pasarlo a el EmailProcessor.