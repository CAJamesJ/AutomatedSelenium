from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_click():
    with open("click_log.txt", "a", encoding="utf-8") as f:
        f.write(request.data.decode("utf-8"))
    return "Logged", 200

if __name__ == "__main__":
    app.run(port=5000)