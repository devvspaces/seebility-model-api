from openai import OpenAI
import time
import os
import json
from . import helpers
from . import utils
from decouple import config


class AssistantManager:
    def __init__(self, api_key, model="gpt-3.5-turbo-1106", functions={"amazon_search": helpers.amazon_search,"walmart_search": helpers.walmart_search, "add_to_cart":helpers.add_to_cart, "get_contact":helpers.get_contact}):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.available_functions = functions
        self.assistant = None
        self.thread = None
        self.run = None

    def create_assistant(self, name, instructions, tools):
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=self.model
        )

    def execute_function_call(self, function_name, arguments):
        function = self.available_functions.get(function_name, None)
        if function:
            arguments = json.loads(arguments)
            results = function(**arguments)
        else:
            results = f"Error: function {function_name} does not exist"
        return results
    def create_thread(self):
        self.thread = self.client.beta.threads.create()

    def create_message_and_run(self, assistant, query):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=query
        )
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        return self.run, self.thread

    def get_function_details(self, run):

        print("\nrun.required_action\n", run.required_action)

        function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
        arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
        function_id = run.required_action.submit_tool_outputs.tool_calls[0].id

        print(f"function_name: {function_name} and arguments: {arguments}")

        return function_name, arguments, function_id

    def submit_tool_outputs(self, run, thread, function_id, function_response):
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=[
                {
                    "tool_call_id": function_id,
                    "output": str(function_response),
                }
            ]
        )
        return run

    def run_assistant(self, transcript):
            self.run, self.thread = self.create_message_and_run(self.assistant, transcript)
            
            while True:
                    run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id, run_id=self.run.id)
                    print("run status", run.status)
                    if run.status == "requires_action":
                        function_name, arguments, function_id = self.get_function_details(
                            run)
                        function_response = self.execute_function_call(
                            function_name, arguments)
                        self.submit_tool_outputs(
                            run, self.thread, function_id, function_response)
                        time.sleep(3)
                        continue

                    if run.status =="failed":
                        text="an error was encountered, kindly retry"
                        print(text)
                        break
                    if run.status == "completed":
                        messages = self.client.beta.threads.messages.list(
                            thread_id=self.thread.id)
                        latest_message = messages.data[0]
                        text = latest_message.content[0].text.value
                        print(text)
                        return text
                        #self.run = None
                        # self.run, self.thread = self.create_message_and_run(self.assistant, tran)
                        

            # time.sleep(1)


def create_manager():
    api_key = config('OPENAI_API_KEY')
    manager = AssistantManager(api_key)
    # create assistant
    manager.create_assistant(
        name="Ecommerce shopping assistant",
        instructions="You are a conversational voice ecommerce shopping assistant, you currently support retail stores amazon and walmart, ensure that you narrow down what exactly the user wants before performing a search , Use the provided functions to answer questions. Synthesise answer based on provided function output in voice output friendly form and be consise not using too many words but communicating effectively, human engagingly also remember not to list the products numerically but in sentence format, eliminate any asterisks and symbols that would obstruct the voice output, never include links in your output, all prices are in dollars and for example if a price is 19000 it should be outputted in the form 190.00",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "amazon_search",
                    "description": "Retrieves the search results given the search query for amazon",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_to_cart",
                    "description": "adds the id of the selected product to cart",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product": {
                                "type": "string",
                                "description": "The id of the selected product to be added to cart"
                            }
                        },
                        "required": ["product"]
                    }
                }
            },
            {
        "type": "function",
        "function": {
            "name": "get_contact",
            "description": "stores contact informaton of user to add them to thw waitlist",
            "parameters": {
                "type": "object",
                "properties": {
                    "contact_info": {
                        "type": "string",
                        "description": "The phone number of the customer"
                    }
                },
                "required": ["contact_info"]
            }
        }
    },
       {
        "type": "function",
        "function": {
            "name": "walmart_search",
            "description": "Retrieves the search results given the search query for walmart ",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
        ]
    )
    manager.create_thread()
    return manager
