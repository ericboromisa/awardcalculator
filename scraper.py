


from lxml import html
import lxml.html
import requests

page = requests.get('http://www.skyscanner.com/transport/flights/sfo/sin/160121/')

tree = html.fromstring(page.content)
print dir(tree)

carriers = tree.xpath('//a[@class="altquotes-action"]/text()')
prices = tree.xpath('//a[@class="mainquote-price big select-action"]/text()')

doc = lxml.html.parse('http://www.skyscanner.com/transport/flights/sfo/sin/160121#results')

print 'Carriers: ', carriers
print 'Prices', prices
print dir(doc)

