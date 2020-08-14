from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q, F
from .models import Video, Category
from user_profile.models import UserProfile


# Create your views here.
def library(request):
    """ a view to to return the landing page """
    if not request.user.is_authenticated:
        return redirect('/')

    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=user)

    videos = Video.objects.all()
    categories = Category.objects.all()
    genre = None
    query = None

    most_viewed = videos.order_by('views').reverse()[0:5]
    popular_categories = categories.order_by('clicks').reverse()[0:3]
    top_category_videos = videos.filter(category=popular_categories[0])[0:5]
    second_category_videos = videos.filter(category=popular_categories[1])[0:5]
    third_category_videos = videos.filter(category=popular_categories[2])[0:4]

    print(top_category_videos)

    if request.GET:
        if 'genre' in request.GET:
            genre = request.GET['genre']

            videos = videos.filter(category__slug__iexact=genre)

            # The statements below increment a click counter in the model
            current_category = categories.get(slug=genre)
            current_category.clicks = F('clicks') + 1
            current_category.save()

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                print('Search query empty')
                return redirect(reverse('library'))
            queries = Q(title__icontains=query) | \
                Q(description__icontains=query)
            videos = videos.filter(queries)

    context = {
        'videos': videos,
        'most_viewed': most_viewed,
        'categories': categories,
        'popular_categories': popular_categories,
        'top_category_videos': top_category_videos,
        'second_category_videos': second_category_videos,
        # 'third_category_videos': third_category_videos,
        'search_term': query,
        'user_profile': user_profile,
    }

    return render(request, 'library/library.html', context)


def player(request, video_id):
    """ a view to return the video player for individual videos """
    if not request.user.is_authenticated:
        return redirect('/')

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    video = get_object_or_404(Video, pk=video_id)

    user_profile.history.add(video)

    video.views = F('views') + 1
    video.save()

    context = {
        'video': video,
    }

    return render(request, 'library/player.html', context)
