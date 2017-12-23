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
#execfile("imageValidation.py")
#endNew

@click.command()
@click.option('--carml_url', default="www.carml.org", help='The URL to the CarML website.')
@click.option('--urls', default='newBear.txt', type=click.File('rb'), help="The file containing all the urls to perform inference on.")
@click.option('--framework_name', default='TensorFlow', help="The framework to use for inference.")
@click.option('--framework_version', default='1.4', help="The framework version to use for inference.")
@click.option('--model_name', default='BVLC-Reference-CaffeNet', help="The model to use for inference.")
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
    count = 1
    lines = urls.readlines()

#output
    outputFile = 'result_bear.txt'
#output to 'result_bear.txt'
#    f = open(outputFile, 'w')
#    f.close()
# data
#    dataBear = open('newBear.txt', 'w')
#    dataBear.close()
#    storeURL = ''
    stopnum = 0
# check url one by one
    urlReq_temp = [{'id': str(uuid.uuid4()), 'data': url.decode("utf-8").strip()}
                    for url in lines[stopnum:]]
    for i in range(len(urlReq_temp)):
		#storeURL = str(lines[i:i+1])
		urlReq = requests.post(urlsAPIURL, json={
			'predictor': openResponseContent,
			'urls': urlReq_temp[i:i+1],
			'options': {
				'feature_limit': 0,
			}
		})
		
		try:
			result = urlReq.json()
		except:		
			print(result)
			continue
		if 'responses' not in result:
                        continue

		if count>1000-stopnum:
			break
		count += 1
		#print(result)#test
		print(str(i) + ': ' + str(count))
#''' find the largest three values '''
		maxValue = [float("-inf"), float("-inf"), float("-inf")]
		resultName = [' ', ' ', ' ']
		if 'responses' in result:
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
        
			f = open(outputFile,'a')
			f.write(data+'\n')
			f.close()

			#add url to new bear
#			dataBear = open('newBear.txt','a')
#			dataBear.write(storeURL+'\n')
#			dataBear.close()
#endOutput

#    dataBear.close()
    requests.post(closeAPIURL, json={'id': predictorId})

if __name__ == "__main__":
    main()
