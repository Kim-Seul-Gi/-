from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Avg
from .models import Movie, Genre, Director
from actors.models import Actor
from accounts.models import *
from accounts.forms import ScoreForm

from django.http import JsonResponse

# Create your views here.
# genre.json import 방법:
# $ python manage.py loaddata genre.json

def show_movies(me):
    out_len = 10
    out = []

    for movie in Movie.objects.all():
        if movie in me.score_set.all():
            continue
        
        man_score = 0.0
        cnt = 0
        for score in movie.movie_scores.all():
            temp = 0
            if Me_you_similar.objects.filter(me = me , you = score.user):
                temp = Me_you_similar.objects.filter(me = me , you = score.user)[0].silmilar
            elif Me_you_similar.objects.filter(me = score.user , you = me):
                temp = Me_you_similar.objects.filter(me = score.user , you = me)[0].silmilar
            temp *= score.score
            man_score += temp
            cnt += 1
                
        if cnt==0 or man_score < 0: continue
        man_score /= cnt
        if len(out)<out_len: out.append([movie,man_score])
        elif out[out_len-1][1] < man_score: out[out_len-1] = [movie,man_score]

        for i in range(len(out)-1,0,-1):
            if out[i][1] > out[i-1][1]: out[i] , out[i-1] = out[i-1] , out[i]
            else: break
    return out #[movie[0] for movie in out]
    
def show_genre():
    out_len = 10
    out = []
    for genre in Genre.objects.all():
        sums = 0
        cnt = 0
        for movie in Movie.objects.filter(genres__in=[genre]):
            for score in Score.objects.filter(movie = movie):
                sums += score.score
                cnt += 1
        if cnt==0: continue
        elif len(out)<out_len: out.append([genre,sums/cnt])
        elif out[out_len-1][1] < sums/cnt: out[out_len-1] = [genre,sums/cnt]
        
        for i in range(len(out)-1,0,-1):
            if out[i][1] > out[i-1][1]: out[i] , out[i-1] = out[i-1] , out[i]
            else: break

    output = []
    for genre in out:
        for movie in Movie.objects.filter(genres__in=[genre[0]]):
            sum_score , score_cnt = 0 , 0
            for score in movie.movie_scores.all():
                sum_score += score.score
                score_cnt+=1
            out_avg = sum_score/score_cnt if score_cnt else 0
            output.append([movie,out_avg])
            if len(output)>=out_len: break
        if len(output)>=out_len: break
    
    return output
        
def show_bestmovies():

    movies_out = {}
    scores = Score.objects.all()
    
    for score in scores:
        movie = score.movie
        score_num = score.score
    
        if movie not in movies_out:
            movies_out.update({f'{movie}':[score_num, 1, score_num]})
        else:
            movies_out[f'{movie}'][0] += score_num
            movies_out[f'{movie}'][1] += 1

    for i in movies_out:
        movies_out[i][2] = movies_out[i][0] / movies_out[i][1]
    
    sorted_movies_out = sorted(movies_out.items(), key=lambda item:item[1][2], reverse=True)
    movies_output = []
    
    for sorted_movie in sorted_movies_out:
        movie = Movie.objects.filter(title=sorted_movie[0]).first()
        movies_output.append([movie, sorted_movie[1][2]])
    
    return movies_output

#-----------------------------------------------------------

def index(request):
    return render(request, 'movies/index.html')

def movie_lists(request):
    
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    movies = show_movies(request.user)
    best_genre = show_genre() # 신욱형이 만든 장르별 영화추천
    best_movies = show_bestmovies() # 김슬기가 만든 영화추천
 
    context = {'movies':movies,'best_genre':best_genre, 'best_movies':best_movies}
    return render(request, 'movies/movies_list.html', context)
    
def movie_detail(request, movie_id):
    
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method=='POST':
        score_form = ScoreForm(request.POST)
        if score_form.is_valid() and request.POST.get('score') and not(movie.movie_scores.filter(user=request.user)):
            score = score_form.save(commit=False)
            # 넘어 온 것 중 그것
            score.score = request.POST.get('score')
            score.movie = movie
            score.user = request.user
            score.save()
            for silmilar in request.user.me_similar.all():
                silmilar.add_movie(movie)
                silmilar.save()
            for silmilar in request.user.you_similar.all():
                silmilar.add_movie(movie)
                silmilar.save()
            
        return redirect('movies:movie_detail', movie_id)
                
    else:
        score_form = ScoreForm()

    context = {'movie':movie, 'score_form':score_form}
    return render(request, 'movies/movie_detail.html', context)
    
def genre_list(request):
    genres = Genre.objects.all()
    context = {'genres':genres}
    return render(request, 'movies/genres_list.html',context)
    
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    context = {'genre':genre}
    return render(request, 'movies/genre_movies.html', context)
    
def director(request, director_id):
    director = get_object_or_404(Director, pk=director_id)
    context = {'director':director}
    return render(request, 'movies/director.html',context)

@login_required       
def movie_evaluate(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    context = {'movies':movies, 'genres':genres}
    return render(request, 'movies/movie_evaluate.html', context)
  
@login_required 
def delete_score(request, movie_id, score_id):
    score = get_object_or_404(Score, pk=score_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.user == score.user:
        for silmilar in request.user.me_similar.all():
            silmilar.remove_movie(movie)
            silmilar.save()
        for silmilar in request.user.you_similar.all():
            silmilar.remove_movie(movie)
            silmilar.save()
        score.delete()
    return redirect('movies:movie_detail', movie_id)


# movies/movielist 에서 영화검색! 쪽에 이름을 올리면 비동기적으로 이름을 포함하고 있는 영화들을 반환합니다.
def search_movie(request, movie_title):
    movies = Movie.objects.filter(title__contains=movie_title)
    print(movies)
    result = list(movies.values())
    return JsonResponse(result, safe=False)
    
# movies/movielist 의 영화검색에서 엔터를 치면 해당 이름을 가지는 영화들을 보여주는 페이지로 이동하기 위해 만든 view-html 함수입니다.
def view_movies(request, movie_title):
    movies = Movie.objects.filter(title__contains=movie_title)
    context = {'movies': movies}
    return render(request, 'movies/view_movies.html', context)


#------------------------------------------------



def out_movie(request):
    context={'out':show_movies()}
    return render(request, 'movies/out_movie.html', context)
    

    



