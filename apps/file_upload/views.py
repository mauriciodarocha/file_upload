"""FILE UPLOAD VIEW"""
# import json
import os
import math
from django.shortcuts import render
from django.middleware.csrf import get_token
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from .models import FileModel, MediaFile


# Create your views here.
def file_upload_view(request):
    """File upload view"""

    return render(request, 'file_upload.html')


def files_list(request):
    """File upload list"""

    page = int(request.GET.get('page') or '1')
    count = int(request.GET.get('count') or '10')

    media_files_all = MediaFile.objects.all().order_by('-date')
    count_max = math.ceil(media_files_all.count() / count)

    previous_page = "&".join(
        [f"page={(1,page - 1)[1 < page]}", f"count={count}"])
    next_page = "&".join(
        [f"page={(page + 1,count_max)[page >= count_max]}", f"count={count}"])

    previous_url = f"?{previous_page}"
    next_url = f"?{next_page}"

    paginator = Paginator(media_files_all, count)

    media_files = paginator.get_page(page)
    media_files_obj = {
        'previous_url': f'{previous_url}',
        'next_url': f'{next_url}',
        'file_url': '/static/',
        'list': media_files,
        'page': page,
        'count': count,
    }

    return render(request, 'file_upload_list.html', media_files_obj)


def upload_file(request):
    """Upload file upload view"""

    file = request.FILES.get('file')

    save_file(file, file.name)

    save_media_info(file.name)

    return HttpResponseRedirect("/media_files/?page=1&count=10")


def upload_file_post(request):
    """Upload file post"""

    file = request.FILES.get('file')
    filename = request.POST.get('filename')
    save_file(file, filename)
    save_media_info(filename)

    url = f"/static/{filename}"

    return JsonResponse({"url": url})


def save_media_info(filename):
    """Save file info in db"""

    filename, filetype = os.path.splitext(filename)
    if filetype:
        filetype = filetype.replace(".", "")
    media_file = MediaFile(name=filename, type=filetype)
    media_file.save()

    return True


def save_file(file, filename):
    """Save file to media folder"""

    fss = FileSystemStorage()
    fss_filename = fss.save(filename, file)
    url = fss.url(fss_filename)

    FileModel.objects.create(doc=url)

    return True


def get_auth_token(request):
    """Get authorizaton token"""
    return JsonResponse({'csrfToken': get_token(request)})
