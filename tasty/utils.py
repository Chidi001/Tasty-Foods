from .models import *

def guestuser(request):

    try:

        customer=Customer.objects.get(device_key= request.session['anony'])
    except:
        request.session['anony']=str(uuid.uuid4())
        customer=Customer.objects.create(device_key = request.session['anony'])
    return{'customer':customer}

