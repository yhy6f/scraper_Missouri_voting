import urllib2, csv
import mechanize
from bs4 import BeautifulSoup

output = open('output.csv', 'w')
writer = csv.writer(output)


br = mechanize.Browser()
br.open('http://enr.sos.mo.gov/EnrNet/CountyResults.aspx')

# Fill out the form
br.select_form(nr=0)
br.form['ctl00$MainContent$cboElectionNames'] = ['750003566']

# Submit the form
br.submit('ctl00$MainContent$btnElectionType')

# Get HTML
html = br.response().read()

# Transform the HTML into a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

dropdown = soup.find('select', id ='cboCounty').find_all('option') #find and find_all are buautifusoup methods

counties = []

for i in dropdown:
	county = {'name':i.text, 'num': i['value']}
	counties.append(county)
	#print county

for county in counties:
    br.select_form(nr=0)
    br.form['ctl00$MainContent$cboCounty'] = [county['num']]
    br.submit('ctl00$MainContent$btnCountyChange')
    html = br.response().read()
    soup = BeautifulSoup(html, "html.parser")

    main_table=soup.find('table', id ='MainContent_dgrdResults')
    print main_table.prettify()

    for row in main_table.find_all('tr'):
        data = [cell.text for cell in row.find_all('td') ]
        if data[0] in ['Hillary Clinton', 'Bernie Sanders','Ted Cruz','John R. Kasich','Donald J. Trump']:
            output.append(data[3])
        writer.writerow(output)




