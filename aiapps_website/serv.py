from flask import Flask, request , render_template
import urllib.request
#from . import CAM_NLU
from CAM_NLU import Extractor

app = Flask(__name__)

@app.route("/", methods =["GET","POST"])
def run():
    if request.method == "POST":
       # getting input with name = input in HTML form
        input = request.form.get("input")
        #print(generateCAMURL("Pepsi", "Coca-Cola", "price"))
        #print(input)
        e = Extractor()
        print(e.extract_comparative(input))
       
        return render_template("form.html") + generateObjAspString(e.extract_comparative(input))
    return render_template("form.html")
    
def generateObjAspString(extracted):
    htmlString = "<!DOCTYPE html><html><head><style>div.container {text-align: center;} ul.myUL {display: inline-block;text-align: left;}</style></head><body><div class=\"container\"><h3>Objects:</h3><ul class=\"myUL\">"

    for object in extracted[0]:
        htmlString += "<li>" + object + "</li>"
    htmlString += "</ul><h3 align=\"center\">Aspects:</h3><ul class=\"myUL\">"
    for aspect in extracted[1]:
        htmlString += "<li>" + aspect + "</li>"
    return htmlString + "</ul></div>"
        



def answer(input):
    #"http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1"
    #print(generateCAMURL)
    fp = urllib.request.urlopen("http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1")
    mybytes = fp.read() 
    

    mystr = mybytes.decode("utf8")
    fp.close()

    return(mystr)

def generateCAMURL(extractedList):
    baseURL = "http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=FS&objectA=OBJA&objectB=OBJB"
    changedURL = baseURL.replace("FS", "false")
    changedURL = changedURL.replace("OBJA", extractedList[0][0])
    changedURL = changedURL.replace("OBJB", extractedList[0][1])
    return appendAspects(changedURL, extractedList[1])

def appendAspects(changedURL, aspectList):
    urlExtension = "&aspect1=ASP1&weight1=WEIGHT1"
    if len(aspectList) == 0:
        return changedURL
    else:
         for count, aspect in enumerate(aspectList, start=1):
            changedURL += "&aspect" + count + "=" + aspect + "&weight" + count +"=" + "1"
    return changedURL