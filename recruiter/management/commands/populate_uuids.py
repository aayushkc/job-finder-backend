# your_app/management/commands/populate_uuids.py

from django.core.management.base import BaseCommand
from recruiter.models import Job
import uuid

class Command(BaseCommand):
    help = 'Populate UUIDs for existing records in MyModel'

    def handle(self, *args, **kwargs):
        records = Job.objects.filter(job_unique_id__isnull=True)
        for record in records:
            record.job_unique_id = uuid.uuid4()
            record.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully populated UUIDs for {records.count()} records'))
