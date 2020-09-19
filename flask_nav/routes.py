from flask import Flask, redirect, render_template, request, session, url_for
app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")
@app.route("/was")
def was():
        return render_template("was.html")
@app.route("/jboss")
def jboss():
        return render_template("jboss.html")
@app.route("/pm2")
def pm2():
        return render_template("pm2.html")
if __name__ == "__main__":
        app.run("0.0.0.0", 5000, debug=True)