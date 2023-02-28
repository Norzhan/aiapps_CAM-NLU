from flask import Flask, request , render_template
import urllib.request

app = Flask(__name__)

@app.route("/", methods =["GET","POST"])
def run():
    if request.method == "POST":
       # getting input with name = input in HTML form
        input = request.form.get("input")
        print(generateCAMURL("Pepsi", "Coca-Cola", "price"))
        return answer(input)
    return render_template("form.html")
    
def answer(input):
    fp = urllib.request.urlopen("http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    return(mystr)

def generateCAMURL(obj1,obj2,aspect):
    baseURL = "http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=FS&objectA=OBJA&objectB=OBJB&aspect1=ASP1&weight1=WEIGHT1"
    changedURL = baseURL.replace("FS", "false")
    changedURL = changedURL.replace("OBJA", obj1)
    changedURL = changedURL.replace("OBJB", obj2)
    changedURL = changedURL.replace("ASP1", aspect)
    changedURL = changedURL.replace("WEIGHT1", "2")
    return changedURL