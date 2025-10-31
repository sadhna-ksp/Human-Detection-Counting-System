import os
import uuid
from django.conf import settings
from django.shortcuts import render
from .detection import detect_by_image, detect_by_video
from .webcam_script import run_webcam_detection  # custom webcam handler

def index(request):
    return render(request, 'index.html')

def process(request):
    mode = request.POST.get('mode')
    upload_dir = settings.MEDIA_ROOT

    if mode == 'image':
        file = request.FILES.get('image')
        if not file:
            return render(request, 'index.html', {'error': 'No image uploaded.'})

        filename = f"{uuid.uuid4().hex}_{file.name}"
        input_path = os.path.join(upload_dir, filename)
        output_path = input_path.replace(".", "_output.")

        with open(input_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        result = detect_by_image(input_path, output_path)
        if not result or not os.path.exists(result):
            return render(request, 'index.html', {'error': 'Image processing failed.'})

        relative_path = os.path.relpath(result, os.path.join(settings.BASE_DIR, 'human_app/static'))
        return render(request, 'result.html', {'result_path': relative_path})

    elif mode == 'video':
        file = request.FILES.get('video')
        if not file:
            return render(request, 'index.html', {'error': 'No video uploaded.'})

        filename = f"{uuid.uuid4().hex}_{file.name}"
        input_path = os.path.join(upload_dir, filename)
        output_path = input_path.replace(".", "_output.")

        with open(input_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        result = detect_by_video(input_path, output_path)
        if not result or not os.path.exists(result):
            return render(request, 'index.html', {'error': 'Video processing failed.'})

        relative_path = os.path.relpath(result, os.path.join(settings.BASE_DIR, 'human_app/static'))
        return render(request, 'result.html', {'result_path': relative_path})

    elif mode == 'webcam':
        run_webcam_detection()
        result_path = 'uploads/webcam_result.jpg'
        return render(request, 'result.html', {'result_path': result_path})

    else:
        return render(request, 'index.html', {'error': 'Invalid mode selected.'})
