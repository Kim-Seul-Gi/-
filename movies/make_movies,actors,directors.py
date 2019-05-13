import datetime
import os
import requests
import csv
import pprint
# from decouple import config

# key = config('TMDB_KEY') 
# 현재는 안됩니다. 그러니까 하지 마세요. 물어보세요 낄낄낄
key = ''

# print(key)

url = f'https://api.themoviedb.org/3/movie/popular?api_key={key}&language=ko-kr&page=1'
            
# # # 1번 풀이 . 여러 날짜에 대해서 {영화 제목:누적관객수, 다른 영화제목:누적관객수}, 이게 1번 풀이, 수정완료

## movie_text에 영화 정보들을 담을 예정입니다.
movie_text={}
response = requests.get(url).json()

results = response['results']
for i in range(len(results)):
    id = results[i]['id']
    title = results[i]['title']
    imageurl = 'https://image.tmdb.org/t/p/w500' + results[i]['poster_path']
    score = int(results[i]['vote_average'])
    release_date = results[i]['release_date']
    overview = results[i]['overview']
    genres = results[i]['genre_ids']
    list = {'id':id,'title':title,
                    'imageurl':imageurl, 'score':score,
                    'release_date':release_date, 'overview':overview,
                    'genres':genres, 'director':''}
    # print(list)
    movie_text.update({f'{id}':list})


actor_text={}
director_text={}

for j in movie_text:
    movie_cord = movie_text[j]['id']
    print(movie_text[j]['id'])
    url2 = f'https://api.themoviedb.org/3/movie/{movie_cord}/credits?api_key={key}'
    response2 = requests.get(url2).json()
    result2 = response2['cast']
    
    # director 관련
    director = response2['crew'][0]   

   
    director_id = director['id']
    director_name = director['name']
    director_imageurl = 'https://image.tmdb.org/t/p/w500' + str(director.get('profile_path'))


    # 여기에서 director 생일 담자
    url4 = f'https://api.themoviedb.org/3/person/{director_id}?api_key={key}&language=en-US'
    response4 = requests.get(url4).json()
    director_birthday = response4['birthday']

    list3 = {'id':director_id, 'name':director_name, 'imageurl':director_imageurl
            , 'birthday':director_birthday }
    director_text.update({f'{director_id}':list3})

    movie_text[f'{movie_cord}']['director'] = director_id



    for k in range(len(result2)):

        if str(result2[k]['id']) in actor_text.keys():
            if not movie_cord in actor_text[str(result2[k]['id'])]['movies']:
                actor_text[str(result2[k]['id'])]['movies'].append(movie_cord)
        else:    
            actor_id = result2[k]['id']
            actor_name = result2[k]['name']
            # acotr_image 도 여기서 추가하도록 하자.
            movies = [movie_cord]

        url5 = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={key}&language=en-US'
        print(url5)
        response5 = requests.get(url5).json()
        actor_birthday = response5['birthday']

        # 여기에서 actor 생일 담자

        list2 = {'id':actor_id, 'name':actor_name, 'birthday':actor_birthday,'movies':movies}
        actor_text.update({f'{actor_id}':list2})    


with open('movies.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['id','title','imageurl',
                    'score','director', 'release_date', 'overview',
                    'genres']
    write=csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for i in movie_text.values():
        write.writerow(i)

with open('actors.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['id','name','birthday', 'movies']
    write=csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for i in actor_text.values():
        write.writerow(i)

with open('directors.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['id','name', 'imageurl','birthday']
    write=csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for i in director_text.values():
        write.writerow(i)