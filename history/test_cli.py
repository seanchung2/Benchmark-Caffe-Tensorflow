# -*- coding: utf-8 -*-

"""Console script for carml_python_client."""

import click
import requests
import chalk
import json
import uuid

#new
#execute the file to check the image existance
import Image
import operator
import httplib
import cStringIO
import urllib
from urlparse import urlparse
execfile("imageValidation.py")
#endNew

@click.command()
@click.option('--carml_url', default="www.carml.org", help='The URL to the CarML website.')
@click.option('--urls', default='example3.txt', type=click.File('rb'), help="The file containing all the urls to perform inference on.")
@click.option('--framework_name', default='Caffe', help="The framework to use for inference.")
@click.option('--framework_version', default='1.0', help="The framework version to use for inference.")
@click.option('--model_name', default='BVLC-GoogLeNet', help="The model to use for inference.")
@click.option('--model_version', default='1.0', help="The model version to use for inference.")
def main(carml_url, urls, framework_name, framework_version, model_name, model_version):
    """Console script for carml_python_client."""
    carml_url = carml_url.strip("/")
    if not carml_url.startswith("http"):
        carml_url = "http://" + carml_url
    openAPIURL = carml_url + "/api/predict/open"
    urlsAPIURL = carml_url + "/api/predict/urls"
    closeAPIURL = carml_url + "/api/predict/close"

    chalk.green("performing inference using " + carml_url)

    click.echo("performing open predictor request on " + openAPIURL)
    openReq = requests.post(openAPIURL, json={
        'framework_name': framework_name,
        'framework_version': framework_version,
        'model_name': model_name,
        'model_version': model_version,
        'options': {
            'execution_options': {
                'batch_size': 1,
                'trace_level': "FULL_TRACE",
            }
        }
    })
    openResponseContent = openReq.json()
    predictorId = openResponseContent["id"]
    click.echo("using the id " + predictorId)

#Edited
#check if the url available
    total = 0
    countImgNum = 0
    correctLine = []
    lines = urls.readlines()
    c = 1#test
    #lines = lines[1430:1431] # 374, 1011, 1139 fail
    lines = lines[1011:1012]
    for index,line in enumerate(lines):
		total = total + 1  	#count how many data in the file
		line = line.rstrip('\\')
		try:
			c = requests.get(line, allow_redirects=False)
			if c.status_code == 404:
				print("in index: " + str(index) + " has a 404")	#find out which index has 404
			if c.status_code == 301:
				print("in index: " + str(index) + " has a 301")
				pass
			if c.status_code < 500:
				try:
					ifile = cStringIO.StringIO(urllib.urlopen(line).read())
					try:
						image = Image.open(ifile)
						print(c)#print('image')
						countImgNum = countImgNum + 1
						print(str(total) + ': ' + str(countImgNum))
						correctLine.append(line)
					except IOError:
						print(str(total) + ': ' + 'not img')
						pass
				except:
					print(str(total) + ': ' + 'error2')
					pass
			else:
				print(str(total) + ': ' + 'error3')
		except requests.ConnectionError:
			print(str(total) + ': ' + 'error4, c = ' + str(c))
			pass

    lines = correctLine  
#endEdited

    urlReq = [{'id': str(uuid.uuid4()), 'data': url.decode("utf-8").strip()}
              for url in lines]
    # print(urlReq)

    urlReq = requests.post(urlsAPIURL, json={
        'predictor': openResponseContent,
        'urls': urlReq,
        'options': {
            'feature_limit': 0,
        }
    })

    print(urlReq.json())

#output
#output to 'result.txt'
    print(countImgNum)
    result = urlReq.json()
#    f = open('result2.txt', 'w')
#    f.close()


#''' find the largest three values '''
    maxValue = [float("-inf"), float("-inf"), float("-inf")]
    resultName = [' ', ' ', ' ']

    for i in result['responses']:
		for j in i['features']:
			if maxValue[0] < j['probability']:
				maxValue[2] = maxValue[1]
				maxValue[1] = maxValue[0]
				maxValue[0] = j['probability']
				resultName[2] = resultName[1]
				resultName[1] = resultName[0]
				resultName[0] = j['name']
			elif maxValue[1] < j['probability']:
				maxValue[2] = maxValue[1]
                                maxValue[1] = j['probability']
                                resultName[2] = resultName[1]
                                resultName[1] = j['name']
			elif maxValue[2] < j['probability']:
                                maxValue[2] = j['probability']
				resultName[2] = j['name']

		data = "{Name:" + str(resultName[0]) + ", Probability:" + str(maxValue[0]) + "} " + " {Name:" + str(resultName[1]) + ", Probability:" + str(maxValue[1]) + "} " + " {Name:" + str(resultName[2]) + ", Probability:" + str(maxValue[2]) + "}"
        
		f = open('result3.txt','a')
		f.write(data+'\n')
		f.close()
		maxValue = float("-inf")
		resultName = ' '
#endOutput

    requests.post(closeAPIURL, json={'id': predictorId})


if __name__ == "__main__":
    main()
