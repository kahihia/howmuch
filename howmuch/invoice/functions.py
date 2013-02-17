from howmuch.invoice.models import Invoice

def get_period():
	pass

#Generar cargo al usuario para determinada asignacion
def generate_charge(assignment, user):
	new_charge = Invoice.objects.create(owner=user, assignment=assignment)
	pass