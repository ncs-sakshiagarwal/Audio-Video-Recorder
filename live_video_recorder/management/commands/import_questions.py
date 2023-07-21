import pandas as pd
from django.core.management.base import BaseCommand
from live_video_recorder.models import Question
import os

class Command(BaseCommand):
    help = 'Import questions from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='question_bank.xlsx')

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), 'question_bank.xlsx')
        df = pd.read_excel(file_path)  # Read the Excel file

        for index, row in df.iterrows():
            question_text = row['Questions']  # Adjust this based on your column name in the Excel file
            # Create a new Question object and save it
            question = Question(question_text=question_text)
            question.save()

        self.stdout.write(self.style.SUCCESS('Questions imported successfully!'))
