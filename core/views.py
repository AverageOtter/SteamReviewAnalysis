from django.shortcuts import render, redirect
# from django.contrib import messages  # Import messages framework for displaying temporary messages
from .forms import InputForm
import steam_ai_package

def home(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['gamename']
            # 
            processed_data = steam_ai_package.get_sentiment_of_game(name)
            # Store the processed data in the session
            request.session['processed_data'] = processed_data
            # Redirect to the same page to avoid form resubmission
            return redirect('home')
    else:
        form = InputForm()
        processed_data = request.session.get('processed_data')  # Retrieve processed data from session
        if processed_data:
            # Delete the processed data from the session after displaying it
            del request.session['processed_data']
            # Add a success message to be displayed after the redirect
            # messages.success(request, 'Form submitted successfully!')

    return render(request, 'index.html', {'form': form, 'processed_data': processed_data})
