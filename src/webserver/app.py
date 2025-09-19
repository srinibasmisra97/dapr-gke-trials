from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/healthcheck", methods=['GET'])
def healthcheck():
  return jsonify({
    'success': True
  })

if __name__=="__main__":
  app.run(host="0.0.0.0", port=8080, debug=False)