import boto3
import click
import botocore

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
def cli():
	"""Common group for all functions"""

@cli.group('volumes')
def volumes():
	"""Commands for volumes"""
	
@cli.group('snapshots')
def snapshots():
	"""Commands for snapshots"""	

@cli.group('instances')
def instances():
	"""Commands for instances"""
	
@snapshots.command('list')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def listInstances(project):
	"List EC2 Snapshots"
	
	instances = filterInstances(project)		
	for e in instances:
		for v in e.volumes.all():
			for s in v.snapshots.all():
				print(" , ".join((e.id,
				e.placement['AvailabilityZone'],
				e.state['Name'],v.volume_id,v.state)))
				
@snapshots.command('create')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def listInstances(project):
	"Create EC2 Snapshots"
	
	instances = filterInstances(project)		
	for e in instances:
		e.stop()
		e.wait_until_stopped()
		for v in e.volumes.all():
			print("Creating snapshot of {0}".format(v.id))
			v.create_snapshot(Description="Created by hawli")
		e.start()
		e.wait_until_running()
	return				
	
@volumes.command('list')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def listInstances(project):
	"List EC2 Volumes"
	
	instances = filterInstances(project)		
	for e in instances:
		for v in e.volumes.all():
			print(" , ".join((e.id,
			e.placement['AvailabilityZone'],
			e.state['Name'],v.volume_id,v.state)))
  
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
		try:
			print("Stopping {0} ..".format(e.id))
			e.stop()
		except botocore.exceptions.ClientError as Ex:
			print("Could not stop {0}".format(e.id) + str(e))
			continue	
	return	
	 	 
@instances.command('start')
@click.option('--project',default=None,help="Only instances for Project (tag Project:<name>)")
def stopInstances(project):
	"Start EC2 Instances"
	instances = filterInstances(project)
	for e in instances:
		try:
			print("Starting {0} ..".format(e.id))
			e.start()
		except botocore.exceptions.ClientError as Ex:
			print("Could not start {0}".format(e.id) + str(e))
			continue
	return	

if __name__ == '__main__':
	
	cli()

