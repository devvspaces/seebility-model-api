import assistant, helpers
test=['hi','i would like an iphone','add the iphone 12 to my cart', '+234809684567']
assistant.create_manager()
assistant.AssistantManager.create_thread()
for i in test:
    assistant.AssistantManager.run_assistant(i)
