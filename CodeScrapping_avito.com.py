import io
import csv
from bs4 import BeautifulSoup
import requests
import re

csv_file = io.open('11-033.csv','w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title','Date','Ad_id','Phonenumber','CategoryID','Category','Region','City','price','subject'])

categoryofavito = ['https://www.avito.ma/fr/maroc/informatique_et_multimedia-%C3%A0_vendre?o={}','https://www.avito.ma/fr/maroc/v%C3%A9hicules-%C3%A0_vendre?o={}','https://www.avito.ma/fr/maroc/immobilier-%C3%A0_vendre?o={}','https://www.avito.ma/fr/maroc/pour_la_maision_et_jardin-%C3%A0_vendre?o={}','https://www.avito.ma/fr/maroc/emploi_et_services-%C3%A0_vendre?o={}']
for cat in categoryofavito :
    for i in range (1,401):

        page = requests.get(cat.format(i))
        soup = BeautifulSoup(page.content , 'html.parser')
        links =soup.find_all(class_='fs14 d-inline-block text-truncate')
        for link in links :
            try:
                title = link.a.text
            except:
                title = None

            link = link.a['href']
            page1 = requests.get(str(link))
            soup1 = BeautifulSoup(page1.content,'html.parser')
            js = soup1.find_all('script', type="text/javascript")
            date = soup1.find(class_="date dtstart value")
            try:
                date = date['title']
            except:
                date = None
            try :
                ad_id = re.search('id..\d+.', str(js)).group().split(':')[1]
            except Exception as e:
                ad_id = None
            try :
                phonenumber = re.search('telephone.*:.*\d+.',str(js), re.I).group().split(':')[1]
            except Exception as e:
                phonenumber = None
            try :
                categoryID = re.search('categoryID.*:.*\d+.',str(js) , re.I).group().split(':')[1]
            except Exception as e:
                categoryID = None
            try :
                region = re.search('region.*:.*\w+.',str(js), re.I).group().split(':')[1]
            except Exception as e:
                region = None
            try :
                category = re.search('category.*:.\w+..',str(js), re.I).group().split(':')[1]
            except Exception as e:
                category = None
            try :
                price = re.search('price.*=.*\d+.',str(js)).group().split('=')[1]
            except Exception as e:
                price = None
            try :
                subject = re.search('subject.*:.*',str(js),re.I).group().split(':')[1]
            except Exception as e:
                subjet = None
            try :
                city = re.search('addressLocality:.*\w+.',str(js),re.I).group().split(':')[1]
            except Exception as e:
                city = None

            csv_writer.writerow([title,date,ad_id,phonenumber,categoryID,category,region,city,price,subject])
        print(i)

csv_file.close()
