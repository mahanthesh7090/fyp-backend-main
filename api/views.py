from django.shortcuts import render
from django.http import JsonResponse
from tweet.models import Tweet, City
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username is None or password is None:
        return JsonResponse({"error": "username or password not provided"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return JsonResponse({"message": "user created successfully"})


def get_tweets_of_city(request, city):
    tweets = Tweet.objects.filter(city__name=city)
    # print(tweets[0].problem_type)
    problem_type = request.GET.get('problem_type', None)
    if problem_type == '' or problem_type == 'All':
        problem_type = None
    
    print(problem_type)
    # print(problem_type)
    if problem_type is not None:
        tweets = tweets.filter(problem_type=problem_type)
    response = []
    for tweet in tweets:
        locations = tweet.location_set.all()
        response.append({
            "id": tweet.id,
            "tweet": tweet.tweet,
            "username": tweet.username,
            "likes": tweet.likes,
            "retweets": tweet.retweets,
            "quotes": tweet.quotes,
            "source": tweet.source,
            "problem_type": tweet.problem_type,
            "media": tweet.media,
            "locations": [location.location for location in locations]
        })

    return JsonResponse({"tweets": response})

def get_names_of_city(request):
    cities = City.objects.all()
    cities = [{"name": city.name, "image": city.image} for city in cities]
    return JsonResponse({"cities": cities})
