import requests
import csv
import os

key = os.getenv('TMDB_KEY')
print(key)
url = f'https://api.themoviedb.org/3/movie/popular?api_key={key}&language=ko-kr&page=1'
            
# # # 1번 풀이 . 여러 날짜에 대해서 {영화 제목:누적관객수, 다른 영화제목:누적관객수}, 이게 1번 풀이, 수정완료

 # movie_text에 영화 정보들을 담을 예정입니다.
movie_text={}
print(url)
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
                    'genres':genres}
    print(list)
    movie_text.update({f'{id}':list})

        
            
with open('movies.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['id','title','imageurl',
                    'score', 'release_date', 'overview',
                    'genres']
    write=csv.DictWriter(f, fieldnames=fieldnames)
    write.writeheader()
    for i in movie_text.values():
        write.writerow(i)
