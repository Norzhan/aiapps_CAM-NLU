from flask import Flask, request , render_template
import urllib.request
#from . import CAM_NLU
from CAM_NLU import Extractor
import webbrowser

app = Flask(__name__)

@app.route("/", methods =["GET","POST"])
def run():
    
    if request.method == "POST":
       # getting input with name = input in HTML form
        input = request.form.get("input")
        #print(generateCAMURL("Pepsi", "Coca-Cola", "price"))
        #print(input)
        e = Extractor(input)
        print(e.extract_comparative())
        if e.check_comparative(input):
            #comparativeHTML = "<div class=\"container\"><br>Your question was found to be comparative.</div>"
            return render_template("results.html",objects = e.extract_comparative()[0], aspects = e.extract_comparative()[1])    #+ comparativeHTML + generateObjAspString(e.extract_comparative()) + "<div class=\"container\"><br>If the extracted objects and/or aspects are not what you expected, <br>please try a different phrasing.</div>"
        else:
            comparativeHTML = "<div class=\"container\"><br>Your question was found to be not comparative.<br>Please ask a comparative question or try a different phrasing.</div>"
            return render_template("non-comparative.html")
        
    return render_template("index.html")
    


    

    
def generateObjAspString(extracted):
    htmlString = "<body><div class=\"container\"><h3 align=\"center\">Objects:</h3><ul class=\"myUL\">"

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

if __name__ == "__main__":
    webbrowser.open_new_tab("http://127.0.0.1:5000")
    #app.run(debug=False, host='0.0.0.0', port=5000)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

    