from flask import Flask, redirect, render_template, request, session, url_for, g
import subprocess
app = Flask(__name__)
app.secret_key = "MySecretKey1234"
@app.before_request
def before_request_func():
    g.ip_addr = "192.168.0.18"
    print("before_request is running!")
 
def api(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    return stdout
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

@app.route("/pm2", methods = ["POST", "GET"])
def pm2_after():
    ip_addr = request.form.get('ip_addr')
    g.ip_addr = ip_addr
    cmd = request.form.get('name')
    print(g.ip_addr)
    cmd1 = "/usr/bin/sshpass -p unbuntu scp -o ConnectTimeout=2 -o StrictHostKeyChecking=no -o LogLevel=Error /tmp/adpass.txt " + ip_addr + ":/tmp"
    subprocess.call(cmd1, shell=True)
    subprocess.call('cp STD_SAMPLE.sh SAMPLE.sh', shell=True)
    with open("SAMPLE.sh", "a") as f:
        f.write(cmd)
    full_cmd = "/usr/bin/sshpass -p unbuntu ssh " + ip_addr + " -o ConnectTimeout=2 -o StrictHostKeyChecking=no -o LogLevel=Error bash -s -- < ./SAMPLE.sh"
    print(full_cmd)
    return render_template("pm2.html", subprocess_output=api(full_cmd))
    subprocess.call(cmd2, shell=True)
 
@app.after_request
def after_request_func(response):
    ip_addr = g.ip_addr
    print(ip_addr)
    cmd2 = "/usr/bin/sshpass -p unbuntu ssh " + ip_addr + " -o ConnectTimeout=2 -o StrictHostKeyChecking=no -o LogLevel=Error rm -rf /tmp/adpass.txt"
    subprocess.call(cmd2, shell=True)
    return response

if __name__ == "__main__":
        app.run("0.0.0.0", 5000, debug=True)
