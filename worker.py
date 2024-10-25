# worker.py
import requests
import time
import json

# Orkes Conductor API URL
CONDUCTOR_API_BASE_URL = "https://play.orkes.io/workflowDef/mental_health_emergency_response"  # replace with your Conductor API URL
CLIENT_ID =  "0ff099b0-92d6-11ef-9ac5-ce590b39fb93"# replace with your client ID
CLIENT_SECRET = "4R5PhtBsODTndhhR2KXMYHBFMPeMI9dD4uFvMZI1f9FmGSlH"# replace with your client secret
TASK_NAME = "EmotionAnalysisWorker"  # replace with your task name in Conductor

def get_jwt_token():
    url = f"{CONDUCTOR_API_BASE_URL}/token"
    payload = {
        "keyId": CLIENT_ID,
        "keySecret": CLIENT_SECRET
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")  # Debugging output

    if response.status_code == 200:
        token = response.json().get("token")
        print("Successfully obtained JWT token.")
        return token
    else:
        print(f"Error obtaining token: {response.status_code} {response.text}")
        return None

# Poll Task
def poll_task(jwt_token):
    url = f"{CONDUCTOR_API_BASE_URL}/tasks/poll/{TASK_NAME}?workerid=worker-1"
    headers = {
        "X-Authorization": jwt_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.text:
        return response.json()
    elif response.status_code == 204:
        print("No tasks available to poll.")
        return None
    else:
        print(f"Error polling task: {response.status_code} {response.text}")
        return None

# A sample function that processes the text to analyze sentiment
def analyze_emotion(text):
    # A basic emotional analysis (this can be extended)
    emotions = {"happy": "positive", "sad": "negative", "angry": "negative"}
    for word, sentiment in emotions.items():
        if word in text.lower():
            return sentiment
    return "neutral"

# Update Task
def update_task(jwt_token, task, result):
    url = f"{CONDUCTOR_API_BASE_URL}/tasks"
    headers = {
        "X-Authorization": jwt_token,
        "Content-Type": "application/json"
    }
    task_update = {
        "taskId": task['taskId'],
        "status": "COMPLETED",
        "outputData": {
            "emotion": result
        }
    }
    response = requests.post(url, json=task_update, headers=headers)
    if response.status_code == 200:
        print("Task updated successfully.")
    else:
        print(f"Error updating task: {response.status_code} {response.text}")

# Main worker loop
def main():
    jwt_token = get_jwt_token()
    if not jwt_token:
        print("Failed to obtain JWT token. Exiting.")
        return

    while True:
        # Poll for a new task
        task = poll_task(jwt_token)
        if task:
            print(f"Processing task: {task['taskId']} with input: {task['inputData']}")
            
            # Process the task input
            input_text = task['inputData'].get('text', '')
            emotion_result = analyze_emotion(input_text)
            
            # Update task with result
            update_task(jwt_token, task, emotion_result)
        else:
            print("No tasks polled. Waiting before next poll.")
        
        # Wait before polling again
        time.sleep(5)

if __name__ == "__main__":
    main()

