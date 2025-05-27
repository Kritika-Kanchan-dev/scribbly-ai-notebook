from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import google.generativeai as genai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import process_file  # your function for summary or flashcard generation
import os

# Configure Gemini API
def configure_gemini():
    try:
        # Try to get API key from settings first
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        
        if not api_key:
            # Fallback: try to get from environment variable directly
            api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("Warning: No Gemini API key found. Please set GOOGLE_API_KEY in your .env file")
            return None
        
        genai.configure(api_key=api_key)
        
        # List of model names to try (in order of preference)
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-1.0-pro',
            'gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-1.0-pro',
            'models/gemini-pro'
        ]
        
        # Try each model name until one works
        for model_name in model_names:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                # Test the model with a simple generation
                test_response = model.generate_content("Hello")
                if test_response:
                    print(f"Successfully configured Gemini API with model: {model_name}")
                    return model
            except Exception as e:
                print(f"Model {model_name} failed: {e}")
                continue
        
        # If no model worked, try to list available models
        try:
            print("Listing available models:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"Available model: {m.name}")
        except Exception as e:
            print(f"Could not list models: {e}")
        
        return None
        
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        return None

# Initialize the model
model = configure_gemini()

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        try:
            # Extract text from the uploaded file (PDF/image)
            extracted_text = process_file(uploaded_file)  # This should return just the text
            
            # Return the extracted text so frontend can put it in the textarea
            return JsonResponse({
                'status': 'success', 
                'extracted_text': extracted_text,
                'message': f'Text successfully extracted from {uploaded_file.name}'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def summarize_flashcard_qa(request):
    if request.method == 'POST':
        # Check if model is configured
        if model is None:
            return JsonResponse({
                'error': 'Gemini API not configured. Please check your API key in the .env file.'
            }, status=500)
        
        task_type = request.POST.get('task')
        user_input = request.POST.get('text')
        question = request.POST.get('question', '')

        if not user_input:
            return JsonResponse({'error': 'No input text provided'}, status=400)

        # Generate appropriate prompt based on task type
        if task_type == 'summarize':
            prompt = f"""Please provide a clear and concise summary of the following text:

{user_input}

Summary:"""
            
        elif task_type == 'flashcards':
            prompt = f"""Create 5 educational flashcards from the following text. Format each flashcard as:

Q1: [Question]
A1: [Answer]

Q2: [Question]
A2: [Answer]

And so on...

Text to create flashcards from:
{user_input}"""
            
        elif task_type == 'qa':
            if not question:
                return JsonResponse({'error': 'No question provided for Q&A task'}, status=400)
            prompt = f"""Based on the following text, please answer the question accurately and in detail.

Text:
{user_input}

Question: {question}

Answer:"""
        else:
            return JsonResponse({'error': 'Invalid task type. Use: summarize, flashcards, or qa'}, status=400)

        try:
            print(f"Sending request to Gemini API for task: {task_type}")
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                return JsonResponse({'result': response.text})
            else:
                return JsonResponse({'error': 'No response generated from API'}, status=500)
                
        except Exception as e:
            print(f"Error generating content: {e}")
            return JsonResponse({'error': f'API Error: {str(e)}'}, status=500)

    # If GET request, redirect back to dashboard
    return redirect('dashboard')

def summarize(request):
    extracted_text = request.session.get('extracted_text', '')
    return render(request, 'summarize.html', {'text': extracted_text})

def home(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html")

def signup_view(request):
    return render(request, "signup.html")

def chat(request):
    return render(request, "chat.html")

def dashboard(request):
    return render(request, "dashboard.html")

@csrf_exempt
def dashboard_process(request):
    """Handle AI processing requests from the dashboard"""
    if request.method == 'POST':
        # Check if model is configured
        if model is None:
            return JsonResponse({
                'error': 'Gemini API not configured. Please check your API key in the .env file.'
            }, status=500)
        
        task_type = request.POST.get('task')
        user_input = request.POST.get('text')
        question = request.POST.get('question', '')

        if not user_input:
            return JsonResponse({'error': 'No input text provided'}, status=400)

        # Generate appropriate prompt based on task type
        if task_type == 'summarize':
            prompt = f"""Please provide a clear and concise summary of the following text:

{user_input}

Summary:"""
            
        elif task_type == 'flashcards':
            prompt = f"""Create 5 educational flashcards from the following text. Format each flashcard as:

Q1: [Question]
A1: [Answer]

Q2: [Question]
A2: [Answer]

And so on...

Text to create flashcards from:
{user_input}"""
            
        elif task_type == 'qa':
            if not question:
                return JsonResponse({'error': 'No question provided for Q&A task'}, status=400)
            prompt = f"""Based on the following text, please answer the question accurately and in detail.

Text:
{user_input}

Question: {question}

Answer:"""
        else:
            return JsonResponse({'error': 'Invalid task type. Use: summarize, flashcards, or qa'}, status=400)

        try:
            print(f"Processing dashboard request for task: {task_type}")
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                return JsonResponse({'result': response.text})
            else:
                return JsonResponse({'error': 'No response generated from API'}, status=500)
                
        except Exception as e:
            print(f"Error generating content: {e}")
            return JsonResponse({'error': f'API Error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def flashcards(request):
    return render(request, "flashcards.html")