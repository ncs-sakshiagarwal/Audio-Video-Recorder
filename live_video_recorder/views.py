import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import redirect, render
from .models import AudioRecording, RecordedVideo, Question, Response, UserProfile, Role
from datetime import datetime
from django.contrib import messages
from django.core.files.base import ContentFile
from pydub import AudioSegment
from django.contrib.auth.decorators import login_required , user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from .decorators import role_required



def record_video(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        new_file_name = 'vid'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_file_name_with_timestamp = new_file_name + '_' + timestamp

        saved_file_path = save_uploaded_file(video, new_file_name_with_timestamp)
        if video:
            recorded_video = RecordedVideo(video=saved_file_path)
            recorded_video.save()
            return JsonResponse({'status': 'success', 'message': 'Recording saved successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No video file received.'})
    return render(request, 'record.html')


def save_uploaded_file(file, name):
    # Generate the full file path with the .webm extension
    file_path = os.path.join(settings.MEDIA_ROOT, name + '.webm')
    
    # Open a file stream in write binary mode
    with open(file_path, 'wb') as destination:
        # Iterate over the chunks of the uploaded file
        for chunk in file.chunks():
            destination.write(chunk)
    
    return file_path


@login_required
@role_required('Job Seeker')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
@role_required('Admin', 'Employer')
def record_list(request):
    record_list = Response.objects.all()
    return render(request, 'record_list.html', {'record_list': record_list})


@login_required
@role_required('Admin', 'Employer')
def question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        Question.objects.create(question_text=question_text)
        return redirect('question')
    else:
        if request.user.username != 'sakshi':
            messages.error(request, "Access denied. You don't have permission to access this page.")
        return render(request, 'question.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('dashboard')


def record_audio(request):
    if request.method == 'POST':
        audio = request.FILES.get('audio')
        new_file_name = 'audio'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_file_name_with_timestamp = new_file_name + '_' + timestamp

        saved_file_path = save_uploaded_file(audio, new_file_name_with_timestamp)
        if audio:
            recorded_audio = AudioRecording(audio=saved_file_path)
            recorded_audio.save()
            return JsonResponse({'status': 'success', 'message': 'Recording saved successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No audio file received.'})
    return render(request, 'record_audio.html')


def save_uploaded_file(file, name):
    # Generate the full file path with the .wav extension
    file_path = os.path.join(settings.MEDIA_ROOT, name + '.wav')
    
    # Open a file stream in write binary mode
    with open(file_path, 'wb') as destination:
        # Iterate over the chunks of the uploaded file
        for chunk in file.chunks():
            destination.write(chunk)
    
    return file_path


@require_GET
def random_question(request):
    # Get a random question from the Question model
    random_question = Question.objects.order_by('?').first()

    # Create a dictionary representation of the question
    question_data = {
        'question_id': random_question.id,
        'question': random_question.question_text,
    }

    # Return the question data as JSON response
    return JsonResponse(question_data)

@csrf_exempt
@permission_required('live_video_recorder.can_record_media')
def submit_response(request):
    if request.method == 'POST':
        response_text = request.POST.get('response_text')
        question_id = request.POST.get('question_id')
        response_type = request.POST.get('response_type')
       
        # Create a new Response instance
        response = Response(response_text=response_text, question_id=question_id)
        if 'video' in request.FILES:
            response_media = request.FILES['video']
        else:
            response_media = request.FILES['audio']
            
        new_file_name = 'media'
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_file_name_with_timestamp = new_file_name + '_' + timestamp

        saved_file_path = save_uploaded_file(response_media, new_file_name_with_timestamp)
        response.response_media = saved_file_path
         # Check the response type
        response.response_type = response_type
        
            # Process video file
        response.user = request.user

        # Save the response
        response.save()

        return JsonResponse({'status': 'success', 'message': 'Response submitted successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
