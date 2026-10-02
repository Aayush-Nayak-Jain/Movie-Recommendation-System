from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
import pyarrow as pa
import json
from database_operation import MovieRecommendationDB

db = MovieRecommendationDB()

movies_data = pd.read_parquet("static/top_2k_movie_data.parquet")
titles = movies_data['title']
titles_list = titles.to_list()
titles_json = json.dumps(titles_list)

def get_recommendations(movie_id_from_db, movie_db):

    try:
        sim_scores = list(enumerate(movie_db[movie_id_from_db]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:16] ## get top 15 Recommendations
        
        movie_indices = [i[0] for i in sim_scores]
        output = movies_data.iloc[movie_indices]
        output.reset_index(inplace=True, drop=True)

        response = []
        for i in range(len(output)):
            response.append({
                'movie_title': output['title'].iloc[i],
                'movie_release_date': output['release_date'].iloc[i],
                'movie_director': output['main_director'].iloc[i],
                'google_link': "https://www.google.com/search?q=" + '+'.join(output['title'].iloc[i].strip().split()) + " (" + output['release_date'].iloc[i].split("-")[0]+")"
            })
        return response
    except Exception as e:
        print("error: ", e)
        return []


def main(request):

    global titles_list, model

    movie_name = request.POST.get('movie_name') or request.GET.get('movie_name')

    if not movie_name:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_json,
                'input_provided': '',
                'movie_found': '',
                'recomendation_found': '',
                'recommended_movies': [],
                'input_movie_name': ''
            }
        )

    movie_name = movie_name.strip()

    if movie_name in titles_list:
        idx = titles_list.index(movie_name)
    else:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_json,
                'input_provided': 'yes',
                'movie_found': '',
                'recomendation_found': '',
                'recommended_movies': [],
                'input_movie_name': movie_name
            }
        )

    # Log search to offline SQLite DB if user is authenticated
    if request.user.is_authenticated:
        db.log_search(request.user.username, movie_name)

    model = pa.parquet.read_table('static/demo_model.parquet').to_pandas()
    final_recommendations = get_recommendations(idx, model)
    if final_recommendations:
        return render(
            request,
            'recommender/result.html',
            {
                'all_movie_names': titles_json,
                'input_provided': 'yes',
                'movie_found': 'yes',
                'recomendation_found': 'yes',
                'recommended_movies': final_recommendations,
                'input_movie_name': movie_name
            }
        )
    else:
        return render(
            request,
            'recommender/index.html',
            {
                'all_movie_names': titles_json,
                'input_provided': 'yes',
                'movie_found': '',
                'recomendation_found': '',
                'recommended_movies': [],
                'input_movie_name': movie_name
            }
        )


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not username or not password:
            messages.error(request, "Username and password cannot be empty.")
            return render(request, 'recommender/signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'recommender/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'recommender/signup.html')

        # Save to SQLite Django Auth DB
        user = User.objects.create_user(username=username, password=password)
        # Also sync/record in standalone MovieRecommendationDB (offline SQLite DB)
        db.create_user(username, password)

        login(request, user)
        messages.success(request, f"Welcome, {username}! Account created successfully.")
        return redirect('main')

    return render(request, 'recommender/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as {username}.")
            return redirect('main')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'recommender/login.html')

    return render(request, 'recommender/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('main')


def history_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in to view your search history.")
        return redirect('login')

    user_history = db.get_search_history(request.user.username)
    return render(request, 'recommender/history.html', {'search_history': user_history})


