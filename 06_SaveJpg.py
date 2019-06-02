import requests


response = requests.get("http://avaimg.nosdn0.126.net/img/NmRMSERweTkzM2Vxd2dKbjNnbjlaNFZ6a29TYkY0N1k1d3BCLy9aK2JxQTlwNUdKdDV2UU9RPT0.jpg")

with open("1.jpg", "wb") as f:
	f.write(response.content)


