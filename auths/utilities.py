from django.contrib.auth.models import User

def generateAlcherId(fullname):
	latUserID = User.objects.latest('id').id
	newUserID=latUserID+1
	fullname_trim = fullname.replace(" ","")
	fullname_trim = fullname_trim.replace("'","")
	fullname_trim = fullname_trim[:3].upper()
	alcher_id= "ALC-"+fullname_trim+"-"+str(newUserID)
	return alcher_id