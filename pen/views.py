import os
import nltk
import spacy
import requests
from bs4 import BeautifulSoup
import language_tool_python
from textstat import textstat
from spellchecker import SpellChecker
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import WritingSubmission

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserReg, Master, WritingSubmission
import chardet


from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserReg, Master, WritingSubmission,FeedbackDetails,Complaint,ChatMessage
import chardet
from django.http import JsonResponse
from django.contrib import messages
from .forms import ComplaintForm
from django.utils import timezone
from django.db.models import Count


# Initialize tools
spell = SpellChecker()
tool = language_tool_python.LanguageTool('en-US')
nlp = spacy.load('en_core_web_sm')

# Known proper nouns
known_proper_nouns = {'Mr.', 'Mrs.', 'Miss', 'Ms.', 'Dr.', 'Emily', 'Blackwood', 'mid-flight',
                      'John', 'Mary', 'London', 'Paris', 'iPhone', 'Google', 'Python',
                      'January', 'Friday', 'Monday', 'Microsoft', 'Apple', 'Android'}

def preprocess_text(text):
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    return sentences, words

def identify_proper_nouns(text):
    doc = nlp(text)
    proper_nouns = [ent.text for ent in doc.ents]
    return proper_nouns

def check_spelling(words, proper_nouns):
    misspelled_words = []
    for word in words:
        if word not in proper_nouns and word not in known_proper_nouns and not spell.correction(word.lower()) == word.lower():
            misspelled_words.append(word)
    return len(misspelled_words), misspelled_words

def check_grammar_and_quotation(sentences):
    grammar_errors = 0
    quotation_issues = []
    error_details = []

    for sentence in sentences:
        matches = tool.check(sentence)
        grammar_errors += len(matches)
        for match in matches:
            error_details.append({
                'sentence': sentence,
                'error': match.message,
                'suggestions': match.replacements
            })

        open_quote = False
        for i, char in enumerate(sentence):
            if char == '"':
                if not open_quote:
                    open_quote = True
                    start_index = i
                else:
                    open_quote = False
                    end_index = i
                    quoted_text = sentence[start_index:end_index+1]
                    quotation_issues.append((quoted_text, start_index, end_index))

        if open_quote:
            quotation_issues.append(("Unclosed quotation mark", len(sentence)-1, len(sentence)-1))

    return grammar_errors, error_details, quotation_issues

def calculate_readability(text):
    return textstat.flesch_kincaid_grade(text)

def check_plagiarism_online(sentence):
    query = f'"{sentence}"'
    url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = soup.find_all('div', class_='yuRUbf')
    return len(results) > 0

def score_text(text):
    sentences, words = preprocess_text(text)
    proper_nouns = identify_proper_nouns(text)
    
    spelling_errors, misspelled_words = check_spelling(words, proper_nouns)
    grammar_errors, grammar_details, quotation_issues = check_grammar_and_quotation(sentences)
    readability_score = calculate_readability(text)
    
    plagiarism_matches = 0
    for sentence in sentences:
        if check_plagiarism_online(sentence):
            plagiarism_matches += 1
    
    plagiarism_percentage = (plagiarism_matches / len(sentences)) * 100
    
    initial_score = 10.0
    spelling_deduction = spelling_errors * 0.5
    score = initial_score - spelling_deduction

    grammar_deduction = grammar_errors * 0.5
    score -= grammar_deduction

    readability_deduction = readability_score * 0.1
    score -= readability_deduction

    plagiarism_deduction = plagiarism_percentage * 0.1
    score -= plagiarism_deduction

    score = max(0, score)

    return {
        "total_score": score,
        "spelling_errors": spelling_errors,
        "misspelled_words": misspelled_words,
        "grammar_errors": grammar_errors,
        "grammar_details": grammar_details,
        "readability_score": readability_score,
        "plagiarism_percentage": plagiarism_percentage,
        "spelling_deduction": spelling_deduction,
        "grammar_deduction": grammar_deduction,
        "readability_deduction": readability_deduction,
        "plagiarism_deduction": plagiarism_deduction
    }

def check_content(request, submission_id):
    submission = get_object_or_404(WritingSubmission, id=submission_id)
    submission.status = 'completed'  # Update status to 'completed' when content checked
    submission.save()

    file_path = submission.file.path
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    results = score_text(content)

    return JsonResponse({'results': results})

def read_file_content(request, submission_id):
    submission = get_object_or_404(WritingSubmission, id=submission_id)
    file_path = submission.file.path
    submission.status = 'opened and under review'  # Make sure 'opened' is a valid choice in your model
    submission.save()
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return render(request, 'display_content.html', {'content': content, 'submission_id': submission_id})


@login_required
def submission_status(request):
    submissions = WritingSubmission.objects.filter(user=request.user)
    return render(request, 'submission_status.html', {'submissions': submissions})


















@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'landing_page.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        qualification = request.POST.get('qualification')
        phone_number = request.POST.get('phone_number')
        location = request.POST.get('location')
        state = request.POST.get('state')
        city = request.POST.get('city')
        image = request.FILES.get('image')

        # Validate passwords
        if password != password1:
            messages.error(request, "Your password and confirm password do not match!")
            return render(request, 'registration.html')

        # Validate phone number
        if len(phone_number) != 10:
            messages.error(request, "Phone number must be exactly 10 digits.")
            return render(request, 'registration.html')

        try:
            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return render(request, 'registration.html')
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'registration.html')

            # Create user
            usr = User.objects.create_user(
                username=username, email=email, password=password, is_active=1)
            usr.save()

            if not image:
                image = 'default/path/to/default/image.jpg'

            par = UserReg.objects.create(
                user=usr, address=address, qualification=qualification,
                phone_number=phone_number, location=location, state=state, city=city, image=image)
            par.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login') 

        except Exception as e:
            messages.error(request, f'Something went wrong: {str(e)}') 

    return render(request, 'registration.html')


def login_user(request):
    next_url = request.GET.get('next', 'home') 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin_dashboard")
            elif user.is_staff:
                data = Master.objects.get(user=user)
                request.session['id'] = data.id
                return redirect(next_url)  # Redirect to next URL or home
            else:
                data = UserReg.objects.get(user=user)
                request.session['id'] = data.id
                return redirect(next_url)  # Redirect to next URL or home
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def coReg(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        password1 = request.POST['password1']
        qual = request.POST['qual']
        field = request.POST['field']
        img = request.FILES.get('img')  

        if password != password1:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('coReg')  

        if not img:
            messages.error(request, 'Image is required. Please select an image to upload.')
            return redirect('coReg')

        
        usr = User.objects.create_user(
            username=username, password=password, is_active=False, is_staff=True)
        usr.save()
        tut = Master.objects.create(username=username, email=email, phone=phone, address=address,
                              qual=qual, field=field, img=img, user=usr)
        tut.save()
        messages.success(request, 'Registration Successful. Please wait for admin approval.')
        return redirect('login')
        

    return render(request, 'coReg.html')


def adminmaster(request):
    msg = ''
    data = Master.objects.all()
    return render(request, 'adminmaster.html', {"data": data, "msg": msg})

@login_required(login_url='login')
def approvemaster(request):
    id = request.GET['id']
    status = request.GET['status']
    data = User.objects.get(id=id)
    data.is_active = status
    data.save()
    return redirect("admin_master_view")

@login_required
def submit_writing(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        if category and title and description and file:
            submission = WritingSubmission(
                user=request.user,
                category=category,
                title=title,
                description=description,
                file=file,
                status='submitted'  
            )
            submission.save()
            return redirect('home')  
        else:
            return render(request, 'submit_writing.html', {'error': 'All fields are required.'})

    return render(request, 'submit_writing.html')


@login_required(login_url='login')
def admin_master_view(request):
    msg = ''
    data = Master.objects.all()
    return render(request, 'master_view_request.html', {"data": data, "msg": msg})
@login_required(login_url='login')
def all_master(request):
    msg = ''
    datas = Master.objects.all()
    return render(request, 'all_master.html', {"datas": datas, "msg": msg})

@login_required(login_url='login')
def all_writters(request):
    msg = ''
    content = UserReg.objects.all()
    return render(request, 'all_writters.html', {"content": content, "msg": msg})
@login_required(login_url='login')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def delete_master(request, master_id):
    master = get_object_or_404(Master, id=master_id)
    master.delete()
    # messages.success(request, 'Master user deleted successfully.')
    return redirect('all_master')


# def view_submissions(request):
#     msg = ''
#     data = UserReg.objects.all()
#     return render(request, 'review_submissions.html', {"data": data, "msg": msg})

def is_staff(user):
    return user.is_staff
@login_required(login_url='login')
@user_passes_test(is_staff)
def view_submissions(request):
    submissions = WritingSubmission.objects.filter(status__in=['submitted', 'opened and under review'])
    return render(request, 'review_submissions.html', {"submissions": submissions})

#accept 
# @login_required(login_url='login')    
def accept_submission(request, submission_id):
    submission = get_object_or_404(WritingSubmission, id=submission_id)
    submission.status = 'open'  # Update status to 'open' when accepted
    submission.save()
    return redirect('submission_status')


def evaluation_page(request):
    accepted_submissions = WritingSubmission.objects.filter(is_accepted=True)
    return render(request, 'evaluation.html', {'submissions': accepted_submissions})

@login_required
def save_feedback(request, submission_id):
    if request.method == 'POST':
        submission = get_object_or_404(WritingSubmission, id=submission_id)
        
        # Extracting and converting values
        spelling_mark = float(request.POST.get('spelling_mark', 0))
        grammar_mark = float(request.POST.get('grammar_mark', 0))
        plagiarism_mark = request.POST.get('plagiarism_mark', '0').replace('%', '')
        total_mark = float(request.POST.get('total_mark', 0))  # Already includes master mark
        master_mark = float(request.POST.get('master_mark', 0))

        # Convert plagiarism_mark to float
        plagiarism_mark = float(plagiarism_mark)
        
        reviewed_by = request.user.username

        # Create FeedbackDetails instance
        FeedbackDetails.objects.create(
            submission=submission,
            spelling_mark=spelling_mark,
            grammar_mark=grammar_mark,
            plagiarism_mark=plagiarism_mark,
            total_mark=total_mark,  # Do not add master mark again
            reviewed_by=reviewed_by
        )
        return redirect('home')  # Change to the appropriate redirect URL

    return redirect('home')


def submission_history(request):
    # Fetch all submissions and prefetch the related feedback details
    submissions = WritingSubmission.objects.prefetch_related('feedbackdetails_set').all()
    
    context = {
        'submissions': submissions,
    }
    
    return render(request, 'submission_history.html', context)


def master_sub_hist(request):
    # Fetch all submissions and prefetch the related feedback details
    submissions = WritingSubmission.objects.prefetch_related('feedbackdetails_set').all()
    
    context = {
        'submissions': submissions,
    }
    
    return render(request, 'master_sub_hist.html', context)

def subm_his_user(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if user is not authenticated

    # Fetch submissions related to the logged-in user and prefetch related feedback details
    submissions = WritingSubmission.objects.filter(user=request.user).prefetch_related('feedbackdetails_set')

    context = {
        'submissions': submissions,
    }
    
    return render(request, 'subm_his_user.html', context)

@login_required
def profile(request):
    user_reg = UserReg.objects.get(user=request.user)
    context = {
        'user': request.user,
        'user_reg': user_reg,
    }
    return render(request, 'profile.html', context)

def edit_profile(request):
    user_reg = UserReg.objects.get(user=request.user)
    
    if request.method == 'POST':
        username = request.POST['username']
        address = request.POST['address']
        email = request.POST['email']
        qualification = request.POST['qualification']
        phone_number = request.POST['phone_number']
        location = request.POST['location']
        state = request.POST['state']
        city = request.POST['city']
        image = request.FILES.get('image', user_reg.image)

        try:
            user = request.user
            user.username = username
            user.email = email
            user.save()
            
            user_reg.address = address
            user_reg.qualification = qualification
            user_reg.phone_number = phone_number
            user_reg.location = location
            user_reg.state = state
            user_reg.city = city
            user_reg.image = image
            user_reg.save()

            return redirect('home')
        except Exception as e:
            return HttpResponse(f"Something went wrong: {e}")

    context = {
        'user': request.user,
        'user_reg': user_reg,
    }
    
    return render(request, 'editprofile.html', context)

@login_required
def master_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    if request.user.is_staff:  # Check if the user is a master (assuming masters are staff users)
        try:
            master_profile = Master.objects.get(user=request.user)
        except Master.DoesNotExist:
            master_profile = None

        return render(request, 'master_profile.html', {'master': master_profile})
    else:
        return redirect('profile')

@login_required
def edit_master_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    if request.user.is_staff:
        master_profile = get_object_or_404(Master, user=request.user)

        if request.method == 'POST':
            master_profile.username = request.POST.get('username', master_profile.username)
            master_profile.email = request.POST.get('email', master_profile.email)
            master_profile.phone = request.POST.get('phone', master_profile.phone)
            master_profile.address = request.POST.get('address', master_profile.address)
            master_profile.qual = request.POST.get('qual', master_profile.qual)
            master_profile.field = request.POST.get('field', master_profile.field)

            # Handle file upload for profile image
            if 'img' in request.FILES:
                master_profile.img = request.FILES['img']

            master_profile.save()
            return redirect('master_profile')  # Redirect to profile page after saving

        return render(request, 'master_edit_profile.html', {'master': master_profile})
    else:
        return redirect('profile')
    

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('home')  # Change 'home' to whatever page you want to redirect to
    else:
        form = ComplaintForm()
    return render(request, 'submit_complaint.html', {'form': form})

@login_required
def view_complaints(request):
    complaints = Complaint.objects.all()
    context = {
        'complaints': complaints
    }
    return render(request, 'view_complaints.html', context)


@login_required
def admin_dashboard(request):
    # Get the total count of Master and UserReg
    total_masters = Master.objects.count()
    total_users = UserReg.objects.count()
    
    # Get weekly data for UserReg and Master
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    weekly_new_masters = Master.objects.filter(user__date_joined__gte=one_week_ago).count()
    weekly_new_users = UserReg.objects.filter(user__date_joined__gte=one_week_ago).count()

    context = {
        'total_masters': total_masters,
        'total_users': total_users,
        'weekly_new_masters': weekly_new_masters,
        'weekly_new_users': weekly_new_users,
    }
    
    return render(request, 'admin_dashboard.html', context)


def admin_dashboard(request):
    total_masters = Master.objects.count()
    total_users = UserReg.objects.count()

    masters_approved = Master.objects.filter(user__is_active=True).count()
    masters_pending = Master.objects.filter(user__is_active=False).count()

    context = {
        'total_masters': total_masters,
        'total_users': total_users,
        'masters_approved': masters_approved,
        'masters_pending': masters_pending,
    }

    return render(request, 'admin_dashboard.html', context)

#chat
def user_chat(request):
    masters = Master.objects.all()
    selected_master = None
    messages = []

    if 'master_id' in request.GET:
        selected_master = get_object_or_404(Master, id=request.GET.get('master_id'))
        messages = ChatMessage.objects.filter(
            (Q(sender_user=request.user.userreg) & Q(receiver_master=selected_master)) |
            (Q(sender_master=selected_master) & Q(receiver_user=request.user.userreg))
        ).order_by('timestamp')

    context = {
        'masters': masters,
        'selected_master': selected_master,
        'messages': messages,
    }
    return render(request, 'userchat.html', context)
from django.db.models import Q

@login_required
def master_chat(request):
    master = get_object_or_404(Master, user=request.user)  # Get the Master object for the logged-in user
    # Get users who have sent messages to the master
    users = UserReg.objects.filter(sent_messages__receiver_master=master).distinct()
    
    selected_user = None
    messages = []

    if 'user_id' in request.GET:
        selected_user = get_object_or_404(UserReg, id=request.GET.get('user_id'))
        # Filter messages between the selected user and the master
        messages = ChatMessage.objects.filter(
            Q(sender_master=master, receiver_user=selected_user) |
            Q(sender_user=selected_user, receiver_master=master)
        ).order_by('timestamp')

    context = {
        'users': users,
        'selected_user': selected_user,
        'messages': messages,
    }
    return render(request, 'masterchat.html', context)

def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        receiver_master_id = request.POST.get('receiver_master_id')
        receiver_user_id = request.POST.get('receiver_user_id')

        if receiver_master_id:
            receiver_master = get_object_or_404(Master, id=receiver_master_id)
            ChatMessage.objects.create(
                sender_user=request.user.userreg,
                receiver_master=receiver_master,
                message=message
            )
            return redirect(f'/user_chat/?master_id={receiver_master_id}')

        if receiver_user_id:
            receiver_user = get_object_or_404(UserReg, id=receiver_user_id)
            ChatMessage.objects.create(
                sender_master=request.user.master,
                receiver_user=receiver_user,
                message=message
            )
            return redirect(f'/master_chat/?user_id={receiver_user_id}')

    # Handle the case where the request method is not POST
    return redirect('user_chat')






# def read_file_content(request, submission_id):
#     submission = get_object_or_404(WritingSubmission, id=submission_id)
#     file_path = submission.file.path

#     with open(file_path, 'rb') as file:
#         raw_data = file.read()
#         result = chardet.detect(raw_data)
#         encoding = result['encoding']
    
#     try:
#         with open(file_path, 'r', encoding=encoding) as file:
#             file_content = file.read()
#     except UnicodeDecodeError:
#         file_content = "Unable to decode file content."

#     return render(request, 'read_file_content.html', {'submission': submission, 'file_content': file_content})


@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    return redirect('login')
