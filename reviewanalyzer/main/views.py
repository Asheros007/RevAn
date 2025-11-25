from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
import json
from django.db.models import Avg
from .models import AnalysisResult

from utilities.sentiment import SentimentAnalyzer

#Views
def landing(request):
    return render(request, 'landing.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used.')
                return redirect('signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username not available!')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password didn't matched!")
            return redirect('signup')
    
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
    
        else:
            messages.info(request, 'Credentials Invalid!')
            return redirect('login')

    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('landing')


@login_required
def dashboard(request):
    # Get user's analyses
    analyses = AnalysisResult.objects.filter(user=request.user)
    
    # Basic counts
    total_analyses = analyses.count()
    positive_count = analyses.filter(overall_sentiment='positive').count()
    negative_count = analyses.filter(overall_sentiment='negative').count()
    neutral_count = analyses.filter(overall_sentiment='neutral').count()
    
    # Calculate percentages
    positive_percentage = round((positive_count / total_analyses * 100) if total_analyses > 0 else 0, 1)
    negative_percentage = round((negative_count / total_analyses * 100) if total_analyses > 0 else 0, 1)
    neutral_percentage = round((neutral_count / total_analyses * 100) if total_analyses > 0 else 0, 1)
    
    # Get recent analyses (last 5)
    recent_analyses = analyses.order_by('-created_at')[:5]
    
    # Calculate average word statistics
    if total_analyses > 0:
        avg_positive_words = analyses.aggregate(avg=Avg('positive_words'))['avg'] or 0
        avg_negative_words = analyses.aggregate(avg=Avg('negative_words'))['avg'] or 0
        avg_neutral_words = analyses.aggregate(avg=Avg('neutral_words'))['avg'] or 0
        
        total_avg_words = avg_positive_words + avg_negative_words + avg_neutral_words
        
        avg_positive_percentage = (avg_positive_words / total_avg_words * 100) if total_avg_words > 0 else 0
        avg_negative_percentage = (avg_negative_words / total_avg_words * 100) if total_avg_words > 0 else 0
        avg_neutral_percentage = (avg_neutral_words / total_avg_words * 100) if total_avg_words > 0 else 0
    else:
        avg_positive_words = avg_negative_words = avg_neutral_words = 0
        avg_positive_percentage = avg_negative_percentage = avg_neutral_percentage = 0
    
    context = {
        'total_analyses': total_analyses,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'recent_analyses': recent_analyses,
        'avg_positive_words': avg_positive_words,
        'avg_negative_words': avg_negative_words,
        'avg_neutral_words': avg_neutral_words,
        'avg_positive_percentage': avg_positive_percentage,
        'avg_negative_percentage': avg_negative_percentage,
        'avg_neutral_percentage': avg_neutral_percentage,
    }
    
    return render(request, 'dashboard.html', context)



@login_required(login_url='login')
def analyze(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        review_text = request.POST.get('review_text')
        review_file = request.FILES.get('review_file')

        if not product_name:
            messages.info(request, 'Product name is required')
            return render(request, 'analyze.html')
        
        if not review_text and not review_file:
            messages.info(request, 'Please provide reviews as text or upload a file.')
            return render(request, 'analyze.html')
        
        if review_file:
            try:
                text = review_file.read().decode('utf-8')
            except Exception as e:
                messages.error(request, f"Error reading file: {e}")
                return render(request, 'analyze.html')
        else:
            text = review_text
            
        request.session['product_name'] = product_name
        request.session['review_text'] = text
        return redirect('result')

    return render(request, 'analyze.html')


@login_required(login_url='login')
def result(request):
    text = request.session.get('review_text')
    product_name = request.session.get('product_name')
    
    if not text or not product_name:
        return redirect('analyze')
    
    analyzer = SentimentAnalyzer()
    analysis = analyzer.comprehensive_analysis(text)
    
    context = {
        'product_name': product_name,
        'review_text': text,
        'analysis': analysis,
        'overview': analysis['overview'],
        'summary': analysis['summary_by_sentiment'],
        'metrics': analysis['detailed_metrics'],
        'word_analysis': analysis['word_analysis']
    }
    
    return render(request, 'result.html', context)


@login_required
def save_analysis(request):
    if request.method == 'POST':
        try:
            def safe_json_parse(json_str, default=None):
                if default is None:
                    default = []
                try:
                    return json.loads(json_str) if json_str else default
                except json.JSONDecodeError:
                    return default

            analysis = AnalysisResult(
                user=request.user,
                product_name=request.POST.get('product_name', ''),
                review_text=request.POST.get('review_text', ''),
                overall_sentiment=request.POST.get('overview_sentiment', 'neutral'),
                sentiment_score=float(request.POST.get('overview_score', 0)),
                
                # Word counts
                total_words=int(request.POST.get('total_words', 0)),
                positive_words=int(request.POST.get('positive_words', 0)),
                negative_words=int(request.POST.get('negative_words', 0)),
                neutral_words=int(request.POST.get('neutral_words', 0)),
                intensifiers=int(request.POST.get('intensifiers', 0)),
                negations=int(request.POST.get('negations', 0)),
                
                # Percentages
                positive_percentage=float(request.POST.get('positive_percentage', 0)),
                negative_percentage=float(request.POST.get('negative_percentage', 0)),
                neutral_percentage=float(request.POST.get('neutral_percentage', 0)),
                
                # Summary data
                positive_summary=request.POST.get('positive_summary', '').split('|||') if request.POST.get('positive_summary') else [],
                negative_summary=request.POST.get('negative_summary', '').split('|||') if request.POST.get('negative_summary') else [],
                neutral_summary=request.POST.get('neutral_summary', '').split('|||') if request.POST.get('neutral_summary') else [],
                
                # Word analysis data - safely parse JSON
                positive_words_list=safe_json_parse(request.POST.get('positive_words_list')),
                negative_words_list=safe_json_parse(request.POST.get('negative_words_list')),
                neutral_words_list=safe_json_parse(request.POST.get('neutral_words_list')),
                intensifiers_list=safe_json_parse(request.POST.get('intensifiers_list')),
                negations_list=safe_json_parse(request.POST.get('negations_list')),
            )
            
            analysis.save()
            
        except Exception as e:
            print("ERROR saving analysis:", str(e))
            import traceback
            traceback.print_exc()  # This will show the full traceback
            messages.error(request, f'Error saving analysis: {str(e)}')
        
        return redirect('history')
    
    return redirect('analyze')


@login_required
def history(request):
    analyses = AnalysisResult.objects.filter(user=request.user).order_by('-created_at')
    
    # Calculate summary statistics
    positive_count = analyses.filter(overall_sentiment='positive').count()
    negative_count = analyses.filter(overall_sentiment='negative').count()
    neutral_count = analyses.filter(overall_sentiment='neutral').count()
    
    context = {
        'analyses': analyses,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
    }
    
    return render(request, 'history.html', context)

@login_required
def delete_analysis(request, analysis_id):
    analysis = get_object_or_404(AnalysisResult, id=analysis_id, user=request.user)
    
    if request.method == 'POST':
        analysis.delete()
        messages.success(request, 'Analysis deleted successfully!')
    
    return redirect('history')

@login_required
def analysis_detail(request, analysis_id):
    # Get the analysis or return 404
    analysis = get_object_or_404(AnalysisResult, id=analysis_id, user=request.user)
    
    context = {
        # Basic info
        'product_name': analysis.product_name,
        'review_text': analysis.review_text,
        
        # Overview data
        'overview': {
            'sentiment': analysis.overall_sentiment,
            'score': analysis.sentiment_score,
        },
        
        # Metrics
        'metrics': {
            'total_words': analysis.total_words,
            'word_counts': {
                'positive': analysis.positive_words,
                'negative': analysis.negative_words,
                'neutral': analysis.neutral_words,
                'intensifiers': analysis.intensifiers,
                'negations': analysis.negations,
            },
            'percentages': {
                'positive': analysis.positive_percentage,
                'negative': analysis.negative_percentage,
                'neutral': analysis.neutral_percentage,
            }
        },
        
        # Summary
        'summary': {
            'positive': analysis.positive_summary,
            'negative': analysis.negative_summary,
            'neutral': analysis.neutral_summary,
        },
        
        # Word analysis
        'word_analysis': {
            'positive_words': analysis.positive_words_list,
            'negative_words': analysis.negative_words_list,
            'neutral_words': analysis.neutral_words_list,
            'intensifiers': analysis.intensifiers_list,
            'negations': analysis.negations_list,
        },
        
        # Flag
        'is_saved_analysis': True
    }
    
    # Use the same template as the analysis results
    return render(request, 'result.html', context)
