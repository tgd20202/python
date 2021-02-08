from flask import Flask
from flask_cors import CORS, cross_origin
import requests
from model.universidades import  Universidades

import requests
from bs4 import BeautifulSoup
import json

from  universidades_crawler import  politecnico, uni_antioquia , itm , politecnico_grancolombiano,ceipa,colegiatura

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


#AIzaSyBFUgorK0CT4v6qobJ-ay-1-TkVOSUK8zY
@app.route('/googleScholar/<tema>')
def googleAcademico(tema):

    urlGoogleAcademico = "https://scholar.google.com/scholar?hl=es&as_sdt=0%2C5&q={}&oq=".format(tema)
    r = requests.get(urlGoogleAcademico)
    print(r.content)

    reponse = []
    for index, item in enumerate(BeautifulSoup(requests.get(urlGoogleAcademico).content, 'lxml').find_all('div', {"class": "gs_r gs_or gs_scl"})):
        reponse.append({
            "id": index,
            "text": item.getText(),
            "urlText":item.find('a', href=True).getText(),
            "url": item.find('a', href=True)['href']
            })
    return json.dumps(reponse)

@app.route('/universidades/<filterCatalogue>')
def universidades(filterCatalogue):
    #poli
    hostUrl="http://prometeo-politecnicojic.hosted.exlibrisgroup.com"
    consturl = hostUrl + "/F/?func=find-b&request=" + filterCatalogue + "&find_code=WRD&adjacent=N&x=32&y=94=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5=";
    #//tr[@valign="baseline"]
    universidades = Universidades(politecnico(filterCatalogue)
                                  ,uni_antioquia(filterCatalogue)
                                  ,itm(filterCatalogue)
                                  ,politecnico_grancolombiano(filterCatalogue),
                                  ceipa(filterCatalogue),
                                  colegiatura(filterCatalogue))

    return json.dumps(universidades.__dict__)




if __name__ == '__main__':
    app.run()