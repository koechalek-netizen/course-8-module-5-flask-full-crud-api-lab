from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
#obtain the JSON data from the request
    data = request.get_json()
#generate a new id for the existing events. If there are no events, the new id will be 1. Otherwise, it will be the maximum id of the existing events plus 1.
    new_id = max(e.id for e in events) + 1 if events else 1
#for creating a new event
    new_event = Event(new_id, data["title"])
#append the new event to the list of events
    events.append(new_event)
#return as json with status code 201(created)
    return jsonify(new_event.to_dict()), 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
#loop through the existing events to find one with matching id 
    for event in events:
        if event.id == event_id:
#if event is found, get new title from the request data and update the event title
            data = request.get_json()
            event.title = data["title"]
#return the updated event as json with status 200
            return jsonify(event.to_dict()), 200
#if the event is not found, return a 404 error with message
    return jsonify({"error": "Event not found"}), 404


#delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
#loop through the existing events to find one with matching id
    for event in events:
        if event.id == event_id:
#if event is found, remove it from the list of events
            events.remove(event)
#return a success message with status 204 (no content)
            return jsonify({"message": "Event deleted successfully"}), 204
#if the event is not found, return a 404 error with message
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
