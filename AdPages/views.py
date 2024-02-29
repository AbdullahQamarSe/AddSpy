from django.shortcuts import render
from django.db.models import Count
from .models import Visitor ,userauthenticate
import stripe
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from bs4 import BeautifulSoup
import re
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import logout

# Create your views here.

@login_required(login_url='login')
def Dashboard(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False

    visitors = Visitor.objects.all()
    visitor_count_by_country = Visitor.objects.values('country_name').annotate(visitor_count=Count('country_name'))
    total_visitors = Visitor.objects.count()

    for visitor_data in visitor_count_by_country:
        visitor_data['percentage'] = (visitor_data['visitor_count'] / total_visitors) * 100

    # Pass the visitor_count_by_country data to the template context
    return render(request, 'dashboard.html', {'visitor_data': visitor_count_by_country,'active_status':active_status , 'user': request.user})


def save_visitor(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        country_name = request.POST.get('country_name')
        coordinates = request.POST.get('coordinates')
        visitor = Visitor.objects.create(ip_address=ip_address, country_name=country_name, coordinates=coordinates)
        visitor.save()
        return JsonResponse({'message': 'Visitor data saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def subscription_limit(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False
    return render(request,"Subscription.html", {'active_status':active_status, 'user': request.user})


@login_required(login_url='login')
def facebook_instagram(request):
    data = []
    first_link=""

    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    
    
    if request.method == 'POST':
        print(request.user.is_subscribe)
        if user.counter > 0 or active_status2:
            user.counter -= 1
            user.save()
        else:
            return redirect(subscription_limit)
        
        search = request.POST.get('search')
        media_type = request.POST.get('media_type')
        country = request.POST.get('country')
        active_status1 = request.POST.get('active_status')
        ad_type = request.POST.get('ad_type')
        print(search,media_type,country,active_status1,ad_type)
        glass = search

        if search == "":
            search = ad_type
            search = search.replace("_", " ")

        print(search)
        secound_search = search.replace(" ", "")
        facebook_page = f"https://www.facebook.com/{secound_search}"
        print(facebook_page)
       
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

        publisher_platforms = request.POST.get('publisher_platforms')
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        base_url = "https://www.facebook.com/ads/library/?active_status={}&ad_type={}&country={}&q={}&publisher_platforms[0]={}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type={}&content_languages[0]=en"

        final_url = base_url.format(active_status1, ad_type, country, search, publisher_platforms, media_type)

        driver.get(final_url)


        try:
            time.sleep(3)
            email_input = driver.find_element(By.ID, "email")
            email_input.send_keys("lksadmlaksdmlaksdm@gmail.com")

            password_input = driver.find_element(By.ID, "pass")
            password_input.send_keys("Sul15871592")

            login_button = driver.find_element(By.CSS_SELECTOR, "[data-testid='royal_login_button']")
            login_button.click()
        except Exception as e:
                print(e)
        try:

            input_field_classes = ".x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.xhk9q7s.x1otrzb0.x1i1ezom.x1o6z2jb.ximmm8s.x1rg5ohu.x1f6kntn.x3stwaq.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1a2a7pz.x6ikm8r.x10wlt62.x1y1aw1k.x1pi30zi.xwib8y2.x1swvt13.x1n2onr6.xlyipyv.xh8yej3.xhtitgo"
            input_field = driver.find_element(By.CSS_SELECTOR, input_field_classes)
            input_field.send_keys(" ")


            # Wait for 4 seconds
            time.sleep(5)

            # Find the button and click
            button_classes = ".x132q4wb "
            button = driver.find_element(By.CSS_SELECTOR, button_classes)

            text = button.find_element(By.CSS_SELECTOR, ".x8t9es0 ")
            linkname = text.text
            linkname_without_spaces = linkname.replace(" ", "")
            search = search.replace(" ", "")

            print("Pokemon",linkname_without_spaces,search)
            print(linkname_without_spaces.lower(),search.lower())
            if linkname_without_spaces.lower() == search.lower():
                print("bothcorrect")
                button.click()
                time.sleep(2)
                driver.current_url
                first_link = driver.current_url
            
            print("not found")
        except Exception as e :
            print(e)

            
        
        driver.get(final_url)
        time.sleep(7)

        driver.execute_script("window.scrollBy(0, 500);")
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        page_name = soup.find_all("div", class_='_7jvw x2izyaf x1hq5gj4 x1d52u69')

        for i in range(len(page_name)):
            try:
                ad_data = {}
                main_section = page_name[i].find_all('div', class_='x1cy8zhl x78zum5 xyamay9 x1pi30zi x18d9i69 x1swvt13 x1n2onr6')
                main_section_data = main_section_elemnent(main_section[0].text)
                if main_section_data:
                    ad_data.update(main_section_data)

                fb_page_name = page_name[i].find('div', class_='_3qn7 _61-0 _2fyi _3qng').text
                ad_data["fb_page_name"] = fb_page_name

                href_link = page_name[i].find('a', class_='xt0psk2 x1hl2dhg xt0b8zv x8t9es0 x1fvot60 xxio538 xjnfcd9 xq9mrsl x1yc453h x1h4wwuj x1fcty0u')['href']
                print("Href link:", href_link)
                ad_data["href_link"] = href_link

                try:
                    ad_description = page_name[i].find("div", class_='_7jyr _a25-').text
                except:
                    ad_description = page_name[i].find("div", class_='_7jyr').text
                ad_data["ad_description"] = ad_description
                
                strt_date = page_name[i].find_all('span', class_='x8t9es0 xw23nyj xo1l8bm x63nzvj x108nfp6 xq9mrsl x1h4wwuj xeuugli')
                print("hi",strt_date[1].text)



                from datetime import datetime

                # Assuming you have already extracted the date string and stored it in strt_date[1].text
                date_str = strt_date[1].text

                # Check if the date string contains a range
                if "-" in date_str:
                    # If it's a range, split it into start and end dates
                    start_date_str, end_date_str = date_str.split(" - ")
                    # Convert start date string to datetime object
                    strt_date = datetime.strptime(start_date_str, "%d %b %Y").date()
                    # Convert end date string to datetime object
                    end_date = datetime.strptime(end_date_str, "%d %b %Y").date()
                else:
                    # If it's not a range, consider it as just a single date
                    # Convert the date string to datetime object
                    strt_date = datetime.strptime(date_str.split("on ")[1], "%d %b %Y").date()
                    # Set end date to current date
                    end_date = datetime.now().date()

                # Now you have start_date and end_date, you can use them as needed
                ad_data["strt_date"] = strt_date
                ad_data["end_date"] = end_date

                duration = end_date - strt_date

                # Calculate weeks and remaining days
                weeks = duration.days // 7
                remaining_days = duration.days % 7

                # Calculate months and remaining days
                months = duration.days // 30
                remaining_days_month = duration.days % 30

                # Construct the duration string
                duration_str = ""
                if weeks > 0:
                    duration_str += f"{weeks} {'week' if weeks == 1 else 'weeks'} "
                if remaining_days > 0:
                    duration_str += f"{remaining_days} {'day' if remaining_days == 1 else 'days'}"
                if months > 0:
                    duration_str += f"{months} {'month' if months == 1 else 'months'} "

                # Determine the score based on the duration
                score = 0
                if weeks < 1:
                    score = 0
                elif weeks <= 2:
                    score = 25
                elif weeks >= 3:
                    score = 40
                elif months >= 1:
                    score = 65
                elif weeks >= 6:
                    score = 75
                elif months >= 2:
                    score = 90

                # Update ad_data with duration string and score
                ad_data["duration"] = duration_str.strip()  # Strip leading/trailing whitespace
                ad_data["score"] = score

                print(strt_date,end_date)
                print(score)

                image = page_name[i].find('img', class_='x1ll5gia x19kjcj4 xh8yej3')
                video = page_name[i].find('video', class_='x1lliihq x5yr21d xh8yej3')
                if image:
                    ad_data["media_url"] = image['src']
                elif video:
                    ad_data["media_url1"] = video['src']

                data.append(ad_data)
            except Exception as e:
                
                print('\n', e)
        print("active status",active_status2)    

    return render(request, 'Facebook&Instagram.html', {'ad_data': data, 'first_link': first_link, 'active_status2':active_status2, 'user': request.user} )

def main_section_elemnent(text):
    pattern = r"Library ID:\s*(\d+).*?(Active).*?Started running on\s*(\d{1,2} \w+ \d{4})"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        library_id = match.group(1)
        status = match.group(2)
        start_date = match.group(3)
        return {
            "library_id": library_id,
            "status": status,
            "start_date": start_date
        }
    else:
        return None
    



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard') 
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')



def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Create a new user
        try:
            user = userauthenticate.objects.create_user(email=email, password=password, name=name)
        except:  # Assuming IntegrityError is raised if email is not unique
            return render(request, 'signup.html', {'error': 'Email is already taken'})

        
        # Optionally, you can log in the user after signup
        login(request, user)
        
        return redirect('dashboard')
    return render(request, 'signup.html')

@login_required(login_url='login')
def google(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False
    return render(request, 'Google.html', {'active_status':active_status, 'user': request.user})

@login_required(login_url='login')
def tiktok(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False
    return render(request, 'TickTok.html', {'active_status':active_status, 'user': request.user})

@login_required(login_url='login')
def youtube(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False
    return render(request, 'Youtube.html', {'active_status':active_status, 'user': request.user})


@login_required(login_url='login')
def subscription_form(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token']
            print("hi", token)
            customer = stripe.Customer.create(
                source=token,
                email=request.user.email
            )
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {'price': 'price_1Om43KEQYK3RMvAppzDAwN5F'},
                ],
            )
            print("hi2", subscription)
            # Update user model with subscription information
            request.user.is_subscribe = True
            request.user.counter = 0
            print(subscription.id)
            request.user.subscription_id = subscription.id
            print(request.user.subscription_id)
            request.user.save()
            Response = "Your Subscription Successful"
            return JsonResponse({'success': False, 'message': Response})
        
        except stripe.error.CardError as e:
            error_msg = str(e)
            print("Welcome")
            print(error_msg)
            Response = error_msg
            return JsonResponse({'success': False, 'message': Response})
        
    return render(request, 'Subscribe.html', {'data': request.user.is_subscribe , 'active_status':active_status , 'user': request.user})

def cancel_subscription(request):
    if request.method == 'POST':
        print("here")
        subscription_id = request.user.subscription_id
        print("here",subscription_id)
        stripe.Subscription.delete(subscription_id)
        print("here",stripe.Subscription.delete)
        # Update user model to reflect cancellation
        request.user.is_subscribe = False
        request.user.subscription_id = None
        request.user.save()
        return HttpResponse("Request cancelled", status=200)
    return HttpResponse("Internal Server Error", status=500)


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def success(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status = subscription['plan']['active']
        print(active_status)
    except:
        active_status = False
    return render(request, 'success.html', {'user': request.user})