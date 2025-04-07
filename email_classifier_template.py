# Configuration and imports
import os
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from llm_service import LLMService
from email_templates import response_templates
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set OpenAI API key
#Open_AI_api_key = os.getenv("OPENAI_API_KEY")

# Sample email dataset
sample_emails = [
    {
        "id": "001",
        "from": "angry.customer@example.com",
        "subject": "Broken product received",
        "body": "I received my order #12345 yesterday but it arrived completely damaged. This is unacceptable and I demand a refund immediately. This is the worst customer service I've experienced.",
        "timestamp": "2024-03-15T10:30:00Z"
    },
    {
        "id": "002",
        "from": "curious.shopper@example.com",
        "subject": "Question about product specifications",
        "body": "Hi, I'm interested in buying your premium package but I couldn't find information about whether it's compatible with Mac OS. Could you please clarify this? Thanks!",
        "timestamp": "2024-03-15T11:45:00Z"
    },
    {
        "id": "003",
        "from": "happy.user@example.com",
        "subject": "Amazing customer support",
        "body": "I just wanted to say thank you for the excellent support I received from Sarah on your team. She went above and beyond to help resolve my issue. Keep up the great work!",
        "timestamp": "2024-03-15T13:15:00Z"
    },
    {
        "id": "004",
        "from": "tech.user@example.com",
        "subject": "Need help with installation",
        "body": "I've been trying to install the software for the past hour but keep getting error code 5123. I've already tried restarting my computer and clearing the cache. Please help!",
        "timestamp": "2024-03-15T14:20:00Z"
    },
    {
        "id": "005",
        "from": "business.client@example.com",
        "subject": "Partnership opportunity",
        "body": "Our company is interested in exploring potential partnership opportunities with your organization. Would it be possible to schedule a call next week to discuss this further?",
        "timestamp": "2024-03-15T15:00:00Z"
    }
]


class EmailProcessor:
    def __init__(self):
        """Initialize the email processor with OpenAI API key."""
        # Define valid categories
        self.valid_categories = {
            "complaint", "inquiry", "feedback",
            "support_request", "other"
        }

        self.llm = LLMService(api_key=os.getenv("OPENAI_API_KEY"))


    def classify_email(self, email: Dict) -> Optional[str]:
        """
        Classify an email using LLM.
        Returns the classification category or None if classification fails.
        
        TODO: 
        1. Design and implement the classification prompt
        2. Make the API call with appropriate error handling
        3. Validate and return the classification
        """
        classification = self.llm.classify(email, self.valid_categories)

        return classification

      
    def generate_response(self, email: Dict, classification: str) -> Optional[str]:
        """
        Generate an automated response based on email classification.
        
        TODO:
        1. Design the response generation prompt
        2. Implement appropriate response templates
        3. Add error handling
        """
        response = self.llm.generate_response(classification, email)
        return response

        


class EmailAutomationSystem:
    def __init__(self, processor: EmailProcessor):
        """Initialize the automation system with an EmailProcessor."""
        self.processor = processor
        self.response_handlers = {
            "complaint": self._handle_complaint,
            "inquiry": self._handle_inquiry,
            "feedback": self._handle_feedback,
            "support_request": self._handle_support_request,
            "other": self._handle_other
        }
        

    def process_email(self, email: Dict) -> Dict:
        """
        Process a single email through the complete pipeline.
        Returns a dictionary with the processing results.
        
        TODO:
        1. Implement the complete processing pipeline
        2. Add appropriate error handling
        3. Return processing results
        """

        classification = None
        sent_response_ok = False

        try: 
            classification = self.processor.classify_email(email)

            if classification is None:

                return {
                    
                    "email_id":email['id'],
                    "success": False,
                    "classification":None,
                    "response_sent":False
                }

            response = self.processor.generate_response(email=email,classification=classification)

            if response is None:

                return {

                    "email_id":email["id"],
                    "success": False,
                    "classification":classification,
                    "response_sent": False
                }
            
            handler = self.response_handlers.get(classification['category'])

            sent_response_ok = handler(email)

            return{

                "email_id":email["id"],
                "success": True,
                "classification":classification,
                "response_sent": sent_response_ok
            }

        except Exception as e:

            logger.error(f"Unable to process the Email {e}") 

            return{

                "email_id":email["id"],
                "success": False,
                "classification": classification,
                "response_sent": sent_response_ok
            }


    def _handle_complaint(self, email: Dict) -> bool:
        """
        Handle complaint emails.
        TODO: Implement complaint handling logic
        """
        try:
            create_urgent_ticket(email_id=email['id'], category='Complaint', context=email['body'])
            send_complaint_response(email_id=email['id'],response=response_templates['complaint'])
            return True
        
        except Exception as e:

            logger.error(f"Urgent ticket creation for email id: {email['id']} has failed {e}")
            return False

        

    def _handle_inquiry(self, email: Dict) -> bool:
        """
        Handle inquiry emails.
        TODO: Implement inquiry handling logic
        """
        try:
            response = self.processor.generate_response(email=email,classification='inquiry')
            send_standard_response(email_id=email['id'], response=response)
            print(f"Response created by the LLM: {response}")
            return True

        except Exception as e:
            
            logger.error(f"Ticket creation for email id: {email['id']}, has failed {e}")
            return False

    def _handle_feedback(self, email: Dict) -> bool:
        """
        Handle feedback emails.
        TODO: Implement feedback handling logic
        """
        try:

            log_customer_feedback(email_id=email['id'], feedback=email['body'])
            send_standard_response(email_id=email["body"],response=response_templates['feedback'])
            return True

        except Exception as e:
    
            logger.error(f"Sending response for email id: {email['id']} has FAILED {e}")
            return False

    def _handle_support_request(self, email: Dict) -> bool:
        """
        Handle support request emails.
        TODO: Implement support request handling logic
        """
        try:
        
            create_support_ticket(email_id=email['id'], context=email['body'])
            send_standard_response(email_id=email['id'], response=response_templates['support_request'])
            return True

        except Exception as e:
            
            logger.error(f"Ticket creation for {email['id']} has FAILED")
            return False

    def _handle_other(self, email: Dict) -> bool:
        """
        Handle other category emails.
        TODO: Implement handling logic for other categories
        """
        try:
            create_urgent_ticket(email_id=email['id'], category='Complaint', context=email['body'])
            send_standard_response(email_id=email['id'],response=self.processor.generate_response(email,classification='other'))
            return True
        
        except Exception as e:

            logger.error(f"Sending response for email id: {email['id']} has FAILED {e}")
            return False


# Mock service functions
def send_complaint_response(email_id: str, response: str):
    """Mock function to simulate sending a response to a complaint"""
    logger.info(f"Sending complaint response for email {email_id}")
    # In real implementation: integrate with email service


def send_standard_response(email_id: str, response: str):
    """Mock function to simulate sending a standard response"""
    logger.info(f"Sending standard response for email {email_id}")
    # In real implementation: integrate with email service


def create_urgent_ticket(email_id: str, category: str, context: str):
    """Mock function to simulate creating an urgent ticket"""
    logger.info(f"Creating urgent ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def create_support_ticket(email_id: str, context: str):
    """Mock function to simulate creating a support ticket"""
    logger.info(f"Creating support ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def log_customer_feedback(email_id: str, feedback: str):
    """Mock function to simulate logging customer feedback"""
    logger.info(f"Logging feedback for email {email_id}")
    # In real implementation: integrate with feedback system


def run_demonstration():
    """Run a demonstration of the complete system."""
    # Initialize the system
    processor = EmailProcessor()
    automation_system = EmailAutomationSystem(processor)

    # Process all sample emails
    results = []
    for email in sample_emails:
        logger.info(f"\nProcessing email {email['id']}...")
        result = automation_system.process_email(email)
        results.append(result)
        print(result)
    # Create a summary DataFrame
    df = pd.DataFrame(results)
    print("\nProcessing Summary:")

    print(df[["email_id", "success", "classification", "response_sent"]])


    return df


# Example usage:
if __name__ == "__main__":

    run_demonstration()