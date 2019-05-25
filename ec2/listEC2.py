import boto3
import click

session = boto3.Session(profile_name='hawli')
ec2 = session.resource('ec2')


def filterInstances(project):
	if project:
		filter = [{'Name':'tag:Test','Values':[project]}]
		instances = ec2.instances.filter(Filters=filter)
		#print(list(instances))
	else:
		instances = ec2.instances.all()	
	return instances	

@click.group()
def instances():
	"""Commands for instances"""

@instances.command('list')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def listInstances(project):
	"List EC2 Instances"
	
	instances = filterInstances(project)		
	for e in instances:
    	 print(" , ".join((e.id,
    	 e.placement['AvailabilityZone'],
    	 e.state['Name']
    	 )))
    #return	 
    	 
@instances.command('stop')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def stopInstances(project):
	"Stop EC2 Instances"
	instances = filterInstances(project)
	for e in instances:
		print("Stopping {0} ..".format(e.id))
		e.stop()
	return	
	 	 
@instances.command('start')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def stopInstances(project):
	"Start EC2 Instances"
	instances = filterInstances(project)
	for e in instances:
		print("Starting {0} ..".format(e.id))
		e.start()
	return	

if __name__ == '__main__':
	
	instances()

