from flask import Flask, jsonify, request
import requests
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

PUBSUB_NAME = "message-pub-sub"
TOPIC = "messages"

URL = "http://localhost:3500/v1.0/publish/%s/%s" % (PUBSUB_NAME, TOPIC)

@app.route("/healthcheck", methods=['GET'])
def healthcheck():
  return jsonify({
    'success': True
  })

@app.route("/post", methods=["POST"])
def post_message():
  request_data = request.get_json()
  result = requests.post(
        url=URL,
        json=request_data
    )
  logging.info('Published data: ' + json.dumps(request_data))
  return jsonify(request_data), result.status_code

if __name__=="__main__":
  app.run(host="0.0.0.0", port=8080, debug=False)