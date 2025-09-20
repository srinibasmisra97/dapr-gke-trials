from flask import Flask, request, jsonify
from cloudevents.http import from_http
import json
import requests

app = Flask(__name__)

STATESTORE="datastore"

URL = "http://localhost:3500/v1.0/state/%s" % (STATESTORE)

# Register Dapr pub/sub subscriptions
@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{
        'pubsubname': 'message-pub-sub',
        'topic': 'messages',
        'route': 'messages'
    }]
    print('Dapr pub/sub is subscribed to: ' + json.dumps(subscriptions))
    return jsonify(subscriptions)


# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/messages', methods=['POST'])
def orders_subscriber():
    event = from_http(request.headers, request.get_data())
    print('Subscriber received : %s' % event.data['orderId'], flush=True)
    response = requests.post(
        URL,
        params={"metadata.contentType": "application/json"},
        json=[{"key": "orderId", "value": event.data['orderId']}],
        headers={"Content-Type": "application/json"}
    )

    return "success",response.status_code


if __name__=="__main__":
  app.run(host="0.0.0.0", port=8081, debug=False)