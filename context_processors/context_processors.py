from video.models import Category, Video


def categories(request):
    category = Category.objects.filter(is_child=False)
    return {"categories": category}


def videos(request):
    video = Video.objects.all()
    return {'video': video}
