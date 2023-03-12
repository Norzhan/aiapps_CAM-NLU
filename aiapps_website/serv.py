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
        #creates an instance of Extractor
        e = Extractor(input)
        #Checks weather the input is a comparative question or not
        if e.check_comparative(input):
            #renders the page to display the extracted objects and aspects
            return render_template("results.html",objects = e.extract_comparative()[0], aspects = e.extract_comparative()[1])
        else:
            #renders th page to display that the question was not found to be comparative
            return render_template("non-comparative.html")    
    #renders the starting page with an inpt field
    return render_template("index.html")
    


    

    
#def generateObjAspString(extracted):
#    htmlString = "<body><div class=\"container\"><h3 align=\"center\">Objects:</h3><ul class=\"myUL\">"
#
#    for object in extracted[0]:
#        htmlString += "<li>" + object + "</li>"
#    htmlString += "</ul><h3 align=\"center\">Aspects:</h3><ul class=\"myUL\">"
#    for aspect in extracted[1]:
#        htmlString += "<li>" + aspect + "</li>"
#    return htmlString + "</ul></div>"
        


#The follwing commented out functions were used to interact with the CAM Backend, 
#a planned but ultimately not included feature
#def answer(input):
    #"http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1"
    #print(generateCAMURL)
#    fp = urllib.request.urlopen("http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=false&objectA=dog&objectB=cat&aspect1=size&weight1=3&aspect2=food&weight2=1")
#    mybytes = fp.read() 
    

#    mystr = mybytes.decode("utf8")
#    fp.close()

#    return(mystr)

#def generateCAMURL(extractedList):
#    baseURL = "http://ltdemos.informatik.uni-hamburg.de/cam-api?fs=FS&objectA=OBJA&objectB=OBJB"
#    changedURL = baseURL.replace("FS", "false")
#    changedURL = changedURL.replace("OBJA", extractedList[0][0])
#    changedURL = changedURL.replace("OBJB", extractedList[0][1])
#    return appendAspects(changedURL, extractedList[1])

#def appendAspects(changedURL, aspectList):
#    urlExtension = "&aspect1=ASP1&weight1=WEIGHT1"
#    if len(aspectList) == 0:
#        return changedURL
#    else:
#         for count, aspect in enumerate(aspectList, start=1):
#            changedURL += "&aspect" + count + "=" + aspect + "&weight" + count +"=" + "1"
#    return changedURL

if __name__ == "__main__":
    webbrowser.open_new_tab("http://127.0.0.1:5000")
    #app.run(debug=False, host='0.0.0.0', port=5000)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

    