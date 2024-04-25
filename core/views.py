from django.shortcuts import render, redirect
# from django.contrib import messages  # Import messages framework for displaying temporary messages
from .forms import InputForm
from .models import SteamGames
from django.utils import timezone
import steam_ai_package
import json

def home(request):
    context = {}
    context["success"] = False
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['gamename']
            app_id = steam_ai_package.get_app_id(name)
            try:
                game = SteamGames.objects.get(app_id=app_id)
                # Check TTL
                if game.TTL <= timezone.now():
                    processed_data = steam_ai_package.get_sentiment_of_game(app_id)
                    game.json_response = processed_data
                    game.TTL = timezone.now() + timezone.timedelta(hours=24)
                    game.save()
                else:
                    processed_data = game.json_response
            except SteamGames.DoesNotExist:
                processed_data = steam_ai_package.get_sentiment_of_game(app_id)
                new_game = SteamGames(app_id=app_id, json_response=processed_data)
                new_game.TTL = timezone.now() + timezone.timedelta(hours=24)
                new_game.save()
            # processed_data = steam_ai_package.get_sentiment_of_game(app_id)
            # Store the processed data in the session
            request.session['processed_data'] = processed_data
            # Redirect to the same page to avoid form resubmission
            return redirect('home')
    else:
        form = InputForm()
        processed_data = request.session.get('processed_data')  # Retrieve processed data from session
        if processed_data:
            processed_data = json.loads(processed_data)
            # Delete the processed data from the session after displaying it
            del request.session['processed_data'] 
            context:dict = processed_data
            context["success"] = True
            with open("output.txt", "w") as file:
                json.dump(processed_data, file, indent=4)
    context['form'] = form
    return render(request, 'index.html', context=context)