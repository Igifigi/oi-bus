from django.core.management.base import BaseCommand
from oi_seattracker.models import Participant, Computer
import json

class Command(BaseCommand):
    help = 'Assigns participants to their computers based on a json file (so-called "autoassign")'
    
    def add_arguments(self, parser):
        parser.add_argument('source_file', type=open)

    def handle(self, *args, **options):
        data = json.load(options['source_file'])
        mapping = {}
        for line in data:
            participant_id = line[0]
            identifier = line[1]
            mapping[participant_id] = identifier

        participants = Participant.objects.all()
        for participant in participants:
            try:
                computer = Computer.objects.get(ip_address=mapping[participant.pk])
            except:
                computer = Computer.objects.get(nice_name=mapping[participant.pk])
            participant.computer = computer
            participant.save()
