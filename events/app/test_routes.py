import json
from fastapi.testclient import TestClient
from event import Event, EventKind
from datetime import datetime
 # Adjust based on the actual FastAPI
from main import app
client = TestClient(app=app)

def test_root():
    response = client.get("/events/meta")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

def test_store():
    formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')[:-3]
    event_payload = dict(user_id=1, user_name='John Doe')
    event = Event(event_id=1, event_name='user_signup_requested', event_creation_ts=formatted_datetime, event_source=EventKind.social_network, event_kind=EventKind.social_network, event_location='social_network', event_processed_ts=formatted_datetime, event_payload=json.dumps(event_payload))
    # Instantiate the Event object
    response = client.put("/events/my_topic/102", json=event.model_dump())
    print(response.json())
    assert response.status_code == 200  # Adjust based on your actual response status code
    # Further assertions can be added based on the expected response

if __name__ == "__main__":
    test_root()
    test_store()
    print("All tests passed!")