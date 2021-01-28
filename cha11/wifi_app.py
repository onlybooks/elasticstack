import urllib.request
from xml.etree.ElementTree import fromstring, ElementTree
from elasticsearch import Elasticsearch

es = Elasticsearch()

#for i in range (4, 5):
for i in range (1, 15):
  iStart = (i-1)*1000 + 1
  iEnd = i*1000

  url = 'http://openapi.seoul.go.kr:8088/(인증키)/xml/PublicWiFiPlaceInfo/'+str(iStart)+'/'+str(iEnd)+'/'
  print(url)
  response = urllib.request.urlopen(url)
  xml_str = response.read().decode('utf-8')
  
  tree = ElementTree(fromstring(xml_str))
  root = tree.getroot()

  for row in root.iter("row"): 
    if row.find('INSTL_Y').text is None:
      instl_y = "0"
    else:
      instl_y = row.find('INSTL_Y').text

    if row.find('INSTL_X').text is None:
      instl_x = "0"
    else:
      instl_x = row.find('INSTL_X').text
  
    try:
      instl_x = float(instl_x)
      instl_y = float(instl_y)
    except ValueError :
      print("error", instl_x, instl_y)
      instl_x = "0"
      instl_y = "0"

    if float(instl_y) < 33 or float(instl_y) > 43 or float(instl_x) < 124 or float(instl_x) > 132:
      instl_y = "0"
      instl_x = "0"    

    if instl_y != "0" and instl_x != "0": 
      doc = {
              "GU_NM": row.find('GU_NM').text,
              "CATEGORY": row.find('CATEGORY').text,
              "PLACE_ADDR": row.find('PLACE_ADDR').text,
              "PLACE_NAME": row.find('PLACE_NAME').text,
              "INSTL_DIV": row.find('INSTL_DIV').text,
              "INSTL_XY": {
                "lat": float(row.find('INSTL_Y').text),
                "lon": float(row.find('INSTL_X').text)
              }
            }
      res = es.index(index='seoul_wifi', doc_type='_doc', body=doc)
      #print(doc)
  print("END", iStart, "~", iEnd)
print("END")