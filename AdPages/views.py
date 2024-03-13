from django.shortcuts import render
from django.db.models import Count
from .models import Visitor ,userauthenticate , Visitor1
import stripe
import json
import datetime
from django.utils.timezone import localtime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from bs4 import BeautifulSoup
import re
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Category, AdminCategory
from datetime import datetime

from django.http import JsonResponse
from .models import Category, AdminCategory
import pycountry


def Location(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False

    from django.utils.timezone import localtime, now
    timezone.activate(settings.TIME_ZONE)
    current_time = now()
    time_only = current_time.strftime('%H:%M:%S')

    print(time_only)
    visitors = Visitor.objects.all()
    for visitor in visitors:
        visitor_time = localtime(visitor.timestamp)
        time_string = visitor_time.strftime('%H:%M:%S')
        time_diff = current_time - visitor_time
        formatted_time_diff = str(time_diff).split('.')[0]  # Extracting hours, minutes, and seconds
        print("Time difference:", formatted_time_diff)
        hours_minutes_seconds = re.match(r'(\d+):(\d+):(\d+)', formatted_time_diff)

        hours = int(hours_minutes_seconds.group(1))
        minutes = int(hours_minutes_seconds.group(2))
        seconds = int(hours_minutes_seconds.group(3))

        total_minutes = hours * 60 + minutes
        print("Visitor:", visitor, "Total minutes:", total_minutes)
        print(type(total_minutes))
        if total_minutes > 6:
            visitor.delete()

    visitors = Visitor.objects.all()



        
    # Initialize a defaultdict to store visitor data by country
    visitor_data_by_country = defaultdict(lambda: {'visitor_count': 0, 'timestamps': [], 'cities': []})

    # Aggregate visitor data by country
    for visitor in visitors:
        country_name = visitor.country_name
        visitor_data_by_country[country_name]['visitor_count'] += 1
        visitor_data_by_country[country_name]['timestamps'].append(visitor.timestamp)
        visitor_data_by_country[country_name]['cities'].append(visitor.city)

    # Calculate total visitors
    total_visitors = sum(data['visitor_count'] for data in visitor_data_by_country.values())

    # Calculate percentage for each country
    for data in visitor_data_by_country.values():
        data['percentage'] = (data['visitor_count'] / total_visitors) * 100

    # Convert defaultdict to list of dictionaries
    visitor_count_by_country = [{'country_name': country_name, 
                                 'visitor_count': data['visitor_count'],
                                 'timestamp': data['timestamps'],
                                 **data} 
                                for country_name, data in visitor_data_by_country.items()]
    
    timezone.activate(settings.TIME_ZONE)
    current_time = timezone.now()
    time_only = current_time.strftime('%H:%M:%S')
    print(time_only)

    # Extract time from timestamp
    print("visting",visitor_count_by_country)

    return JsonResponse(visitor_count_by_country, safe=False)
        
def get_categories(request):
    admin_category_name = request.GET.get('admin_category_name')
    if admin_category_name:
        categories = Category.objects.filter(country=admin_category_name)
        data = [{'name': category.name} for category in categories]
    else:
        # If no admin category is selected, return default category or categories for "United States"
        default_categories = Category.objects.filter(country='United States')  # Assuming 'United States' is the default
        data = [{'name': category.name} for category in default_categories]
    return JsonResponse(data, safe=False)



def admin_category_dropdown(request):
    admin_categories = AdminCategory.objects.all()
    return render(request, 'admin_category_dropdown.html', {'admin_categories': admin_categories})



@login_required(login_url='login')
def Profile(request):
    user = request.user
    stripe.api_key = "sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao"
    print(user.name)
    print(user.subscription_id)

    return render(request, 'profile&account.html',{'user': user})



@login_required(login_url='login')
def change_name(request):
    change_name_error = None
    if request.method == 'POST':
        user = request.user
        new_name = request.POST.get('name')
        if new_name:
            user.name = new_name
            user.save()
        else:
            change_name_error = "Name cannot be empty."
    return render(request, 'profile&account.html', {'change_name_error': change_name_error, 'user': user})

@login_required(login_url='login')
def change_password(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False

    change_password_error = None

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        print(old_password,new_password1,new_password2)

        if new_password1 != new_password2:
            change_password_error = "New passwords do not match."
            return render(request, 'profile&account.html', {'active_status2':active_status2, 'change_password_error': change_password_error})

        else:
            user = request.user
            form = PasswordChangeForm(user, {'old_password': old_password, 'new_password1': new_password1, 'new_password2': new_password2})

            # Check if the old password provided by the user is correct
            if user.check_password(old_password):
                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)  # Important for maintaining session
                    messages.success(request, 'Your password was successfully updated!')
                    return redirect('profile')
                else:
                    change_password_error = "Your Old Password is Short (Minimum 8 Characters)"
            else:
                change_password_error = "Incorrect old password provided."

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile&account.html', {'active_status2':active_status2,'form': form, 'change_password_error': change_password_error})



from collections import defaultdict

def Dashboard(request):
    if not request.user.is_authenticated:
        return redirect(freeDashboard)
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False

    # Get visitor data
    visitors = Visitor1.objects.all()

    # Initialize a defaultdict to store visitor data by country
    visitor_data_by_country = defaultdict(lambda: {'visitor_count': 0, 'timestamps': [], 'cities': []})

    # Aggregate visitor data by country
    for visitor in visitors:
        country_name = visitor.country_name
        visitor_data_by_country[country_name]['visitor_count'] += 1
        visitor_data_by_country[country_name]['timestamps'].append(visitor.timestamp)
        visitor_data_by_country[country_name]['cities'].append(visitor.city)

    # Calculate total visitors
    total_visitors = sum(data['visitor_count'] for data in visitor_data_by_country.values())

    # Calculate percentage for each country
    for data in visitor_data_by_country.values():
        data['percentage'] = (data['visitor_count'] / total_visitors) * 100

    # Convert defaultdict to list of dictionaries
    visitor_count_by_country = [{'country_name': country_name, **data} for country_name, data in visitor_data_by_country.items()]

    print(visitor_count_by_country)

    return render(request, 'dashboard.html', {'visitor_data': visitor_count_by_country, 'active_status2': active_status2, 'user': request.user,})


import pycountry

def save_visitor(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        country_code = request.POST.get('country_name')  # Assuming country_code is received instead of country name
        coordinates = request.POST.get('coordinates')
        city = request.POST.get('city')

        # Lookup country name from country code
        country_name = None
        try:
            country_name = pycountry.countries.get(alpha_2=country_code).name
        except AttributeError:
            pass  # Handle the case where country code is invalid or not found

        # Create and save visitor
        visitor1 = Visitor1.objects.create(ip_address=ip_address, country_name=country_name, coordinates=coordinates, city=city)
        visitor1.save()

        visitor = Visitor.objects.create(ip_address=ip_address, country_name=country_name, coordinates=coordinates, city=city)
        visitor.save()
        return JsonResponse({'message': 'Visitor data saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

@login_required(login_url='login')  
def subscription_limit(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request,"Subscription.html", {'active_status2':active_status2, 'user': request.user})


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
            print("error")
            return JsonResponse({'error': 'Required data missing'}, status=400)
        
        Optimized = request.POST.get('Optimized')
        search = request.POST.get('search')
        media_type = request.POST.get('media_type')
        country = request.POST.get('admin-category-dropdown')
        pk_value = request.POST.get('pk_value')

        print(f"Optimized: {Optimized}")
        print(f"Search: {search}")
        print(f"Media Type: {media_type}")
        print(f"Country: {country}")

        import datetime

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if Optimized == '90':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")  # 2 months previous
            end_date = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
        elif Optimized == '75':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")  # 6 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=6)).strftime("%Y-%m-%d")
        elif Optimized == '65':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=6)).strftime("%Y-%m-%d")
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime("%Y-%m-%d")
        elif Optimized == '40':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime("%Y-%m-%d")  # 3 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")
        elif Optimized == '25':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")  # 2 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=2)).strftime("%Y-%m-%d")
        elif Optimized == '0':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=2)).strftime("%Y-%m-%d")  # 1 day previous
            end_date = current_date
        else:
            start_date_min = current_date

        try:
            country = pycountry.countries.lookup(country).alpha_2
            print("Country Code:", country)
        except LookupError:
            print("Country not found")

        active_status1 = "active"
        categories = ['all', 'credit_ads', 'employment_ads', 'housing_ads', 'political_and_issue_ads']

        # Get the ad_type from request.POST
        ad_type = request.POST.get('category-dropdown')
        if ad_type == "All ads":
            ad_type = "all"

        if ad_type == "Issues, elections or politics":
            ad_type = "political_and_issue_ads"

        if ad_type == "Properties":
            ad_type = "housing_ads"

        if ad_type == "Employment":
            ad_type = 'employment_ads'

        if ad_type == "Credit":
            ad_type = 'credit_ads'

        print("ad_type",ad_type)
        print("working or not check",country,ad_type)

        print(search,media_type,country,active_status1,ad_type)
        glass = search

        if search == "":
            search = ad_type
        
        if ad_type != "":
            search = ad_type

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

        publisher_platforms = request.POST.get('publisher_platforms')
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        base_url = "https://www.facebook.com/ads/library/?active_status={}&ad_type={}&country={}&q={}&publisher_platforms[0]={}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={}&start_date[max]={}&search_type=keyword_unordered&media_type={}&content_languages[0]=en"

        
        final_url = base_url.format(active_status1, "all", country, search, publisher_platforms, start_date_min, end_date, media_type)

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

        if pk_value == '1':
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
            
        time.sleep(2)
        if pk_value == '1':
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(500, 1000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1000, 1500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1500, 2500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(2500, 3500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(3500, 4500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(4500, 5500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(5500, 6500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(6500, 7500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(7500, 8500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(8500, 9500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(9500, 10500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(10500, 11500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(11500, 12500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(12500, 13500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(13500, 14500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(14500, 15500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(15500, 16500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(16500, 17500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(17500, 18500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(18500, 19500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(19500, 20000);")
        elif pk_value == '2':
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(500, 1000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1000, 1500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1500, 2500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(2500, 3500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(3500, 4500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(4500, 5500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(5500, 6500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(6500, 7500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(7500, 8500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(8500, 9500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(9500, 10500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(10500, 11500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(11500, 12500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(12500, 13500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(13500, 14500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(14500, 15500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(15500, 16500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(16500, 17500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(17500, 18500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(18500, 19500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(19500, 20000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(20000, 21000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(21000, 22000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(22000, 23000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(23000, 24000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(24000, 25000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(25000, 26000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(26000, 27000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(27000, 28000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(28000, 29000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(29000, 30000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(30000, 31000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(31000, 32000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(32000, 33000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(33000, 34000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(34000, 35000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(35000, 36000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(36000, 37000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(37000, 38000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(38000, 39000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(39000, 40000);")

        time.sleep(2)
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

                

                # Update ad_data with duration string and score
                ad_data["duration"] = duration_str.strip()  # Strip leading/trailing whitespace
                ad_data["score"] = Optimized
                print(Optimized)
                print(ad_data["score"],"ad_data['score']")


                image = page_name[i].find('img', class_='x1ll5gia x19kjcj4 xh8yej3')
                video = page_name[i].find('video', class_='x1lliihq x5yr21d xh8yej3')
                if image:
                    ad_data["media_url"] = image['src']
                elif video:
                    ad_data["media_url1"] = video['src']
                print("Optimized:", Optimized, type(Optimized))

                if not any(ad["href_link"] == ad_data["href_link"] for ad in data):
                    data.append(ad_data)

            except Exception as e:
                
                print('\n', e)
                
        print("active status",active_status2)   
        data_dict = {
            'ad_data': data,
            'first_link': first_link,
            'active_status2': active_status2,
            'user': str(request.user)
        }
        return JsonResponse(data_dict)
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
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request, 'Google.html', {'active_status2':active_status2, 'user': request.user})

@login_required(login_url='login')
def tiktok(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request, 'TickTok.html', {'active_status2':active_status2, 'user': request.user})

@login_required(login_url='login')
def youtube(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request, 'Youtube.html', {'active_status2':active_status2, 'user': request.user})


@login_required(login_url='login')
def subscription_form(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    
    try:
        card_details = []
        invoices_data = []
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        if request.user.customer_id:
            invoices = stripe.Invoice.list(customer=request.user.customer_id)
            for invoice in invoices:
                invoice_data = {
                    "id": invoice.id,
                    "amount_due": invoice.amount_due / 100,
                    "currency": invoice.currency,
                    "due_date": invoice.due_date,
                    "status": invoice.status,
                    "period_start": invoice.period_start,
                    "period_end": invoice.period_end,
                }
                invoices_data.append(invoice_data)
            customer = stripe.Customer.retrieve(request.user.customer_id)
            print(customer)
            default_payment_method_id = customer.default_source
            print(default_payment_method_id)
        

        if default_payment_method_id is not None:
            default_payment_method = stripe.PaymentMethod.retrieve(default_payment_method_id)
            
            brand = default_payment_method["card"]["brand"]
            name = default_payment_method["billing_details"]["name"]
            exp_month = default_payment_method["card"]["exp_month"]
            exp_year = default_payment_method["card"]["exp_year"]
            last4 = default_payment_method["card"]["last4"]

            card_details.append(brand)
            card_details.append(name)
            card_details.append(exp_month)
            card_details.append(exp_year)
            card_details.append(last4)

    except Exception as e:
        print("nothing",e)
        invoices = None

    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
        
    except:
        active_status2 = False

    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token']
            print("token",token)
            owner_name = data['owner']

            
            if not request.user.customer_id:
                customer = stripe.Customer.create(
                    source=token,
                    email=request.user.email,
                    name=owner_name  # Pass owner name to Stripe
                )
                request.user.customer_id = customer.id
                request.user.save()
                
                subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[
                        {'price': 'price_1OsDT2EQYK3RMvAp3P8tdDT7'},
                    ],
                )

            if not request.user.First:
                subscription = stripe.Subscription.create(
                    customer=customer.id,
                    items=[
                        {'price': 'price_1OsDT2EQYK3RMvAp3P8tdDT7'},
                    ],
                    trial_period_days=60
                )

            if request.user.First:

                subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {'price': 'price_1OsDT2EQYK3RMvAp3P8tdDT7'},
                ],
                )
                
            print(subscription.id)
            request.user.is_subscribe = True
            request.user.counter = 0
            
            request.user.subscription_id = subscription.id
            request.user.save()
            Response = "Your Subscription Successful"

            return JsonResponse({'success': True, 'message': Response})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    print(request.user.customer_id)
    print("Hello",invoices)
    print(card_details )
    return render(request, 'Subscribe.html', {'data': request.user.is_subscribe , 'active_status2':active_status2 , 'user': request.user, 'invoices_data':invoices_data , 'card':card_details })



@login_required(login_url='login')
def update_card(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False

    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(request.user.subscription_id)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data['token']
            owner_name = data['owner']
            print(owner_name,"hi")
            customer_id = request.user.customer_id
            stripe.api_key = settings.STRIPE_SECRET_KEY
            print(request.user.email)
            print(customer_id)
            response = stripe.Customer.modify(
                customer_id,
                source=token,
            )
            print(response)
            return JsonResponse({'success': True, 'message': 'Card updated successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)})
    return render(request, 'update_card.html', {'data': request.user.is_subscribe , 'active_status2':active_status2 , 'user': request.user})


def cancel_subscription(request):
    if request.method == 'POST':
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        print("here")
        subscription_id = request.user.subscription_id
        print("here",subscription_id)
        stripe.Subscription.delete(subscription_id)
        print("here",stripe.Subscription.delete)
        # Update user model to reflect cancellation
        request.user.is_subscribe = False
        request.user.subscription_id = None
        request.user.First = True
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
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request, 'success.html', {'user': request.user})

@login_required
def success1(request):
    user = request.user
    usersubscribe = request.user.subscription_id
    try:
        stripe.api_key = 'sk_test_51M1RZSEQYK3RMvApDzbiHMTOBZUypqMeAtpoyqhLAbmvCDMP71ulYUPGR68CvZpTM0CNGcPT9kJhJPY3C7YFtReI00Tw4Tc6ao'
        subscription = stripe.Subscription.retrieve(usersubscribe)
        active_status2 = subscription['plan']['active']
        print(active_status2)
    except:
        active_status2 = False
    return render(request, 'success1.html', {'user': request.user})




def freeDashboard(request):

    data = []
    first_link=""
    session_limit_key = 'subscription_limit'
    if 'counter' not in request.session:
        request.session['counter'] = 2


    
    if request.method == 'POST':
        if request.session['counter'] >= 0:
            request.session['counter'] -= 1
            request.session.modified = True
        else:
            return JsonResponse({'error': 'Required data missing'}, status=400)
        
        Optimized = request.POST.get('Optimized')
        search = request.POST.get('search')
        media_type = request.POST.get('media_type')
        country = request.POST.get('admin-category-dropdown')
        pk_value = request.POST.get('pk_value')

        print(f"Optimized: {Optimized}")
        print(f"Search: {search}")
        print(f"Media Type: {media_type}")
        print(f"Country: {country}")

        import datetime

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        if Optimized == '90':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")  # 2 months previous
            end_date = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
        elif Optimized == '75':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")  # 6 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=6)).strftime("%Y-%m-%d")
        elif Optimized == '65':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=6)).strftime("%Y-%m-%d")
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime("%Y-%m-%d")
        elif Optimized == '40':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=4)).strftime("%Y-%m-%d")  # 3 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")
        elif Optimized == '25':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=3)).strftime("%Y-%m-%d")  # 2 weeks previous
            end_date = (datetime.datetime.now() - datetime.timedelta(weeks=2)).strftime("%Y-%m-%d")
        elif Optimized == '0':
            start_date_min = (datetime.datetime.now() - datetime.timedelta(weeks=2)).strftime("%Y-%m-%d")  # 1 day previous
            end_date = current_date
        else:
            start_date_min = current_date

        try:
            country = pycountry.countries.lookup(country).alpha_2
            print("Country Code:", country)
        except LookupError:
            print("Country not found")

        active_status1 = "active"
        categories = ['all', 'credit_ads', 'employment_ads', 'housing_ads', 'political_and_issue_ads']

        # Get the ad_type from request.POST
        ad_type = request.POST.get('category-dropdown')
        if ad_type == "All ads":
            ad_type = "all"

        if ad_type == "Issues, elections or politics":
            ad_type = "political_and_issue_ads"

        if ad_type == "Properties":
            ad_type = "housing_ads"

        if ad_type == "Employment":
            ad_type = 'employment_ads'

        if ad_type == "Credit":
            ad_type = 'credit_ads'

        print("ad_type",ad_type)
        print("working or not check",country,ad_type)

        print(search,media_type,country,active_status1,ad_type)
        glass = search

        if search == "":
            search = ad_type
        
        if ad_type != "":
            search = ad_type

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)

        publisher_platforms = request.POST.get('publisher_platforms')
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        base_url = "https://www.facebook.com/ads/library/?active_status={}&ad_type={}&country={}&q={}&publisher_platforms[0]={}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={}&start_date[max]={}&search_type=keyword_unordered&media_type={}&content_languages[0]=en"

        
        final_url = base_url.format(active_status1, "all", country, search, publisher_platforms, start_date_min, end_date, media_type)

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

        if pk_value == '1':
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
            
        time.sleep(2)
        if pk_value == '1':
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(500, 1000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1000, 1500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1500, 2500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(2500, 3500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(3500, 4500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(4500, 5500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(5500, 6500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(6500, 7500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(7500, 8500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(8500, 9500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(9500, 10500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(10500, 11500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(11500, 12500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(12500, 13500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(13500, 14500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(14500, 15500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(15500, 16500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(16500, 17500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(17500, 18500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(18500, 19500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(19500, 20000);")
        elif pk_value == '2':
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(500, 1000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1000, 1500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(1500, 2500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(2500, 3500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(3500, 4500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(4500, 5500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(5500, 6500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(6500, 7500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(7500, 8500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(8500, 9500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(9500, 10500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(10500, 11500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(11500, 12500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(12500, 13500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(13500, 14500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(14500, 15500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(15500, 16500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(16500, 17500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(17500, 18500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(18500, 19500);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(19500, 20000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(20000, 21000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(21000, 22000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(22000, 23000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(23000, 24000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(24000, 25000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(25000, 26000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(26000, 27000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(27000, 28000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(28000, 29000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(29000, 30000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(30000, 31000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(31000, 32000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(32000, 33000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(33000, 34000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(34000, 35000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(35000, 36000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(36000, 37000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(37000, 38000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(38000, 39000);")
            time.sleep(1)
            driver.execute_script("window.scrollBy(39000, 40000);")

        time.sleep(2)
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

                

                # Update ad_data with duration string and score
                ad_data["duration"] = duration_str.strip()  # Strip leading/trailing whitespace
                ad_data["score"] = Optimized
                print(Optimized)
                print(ad_data["score"],"ad_data['score']")


                image = page_name[i].find('img', class_='x1ll5gia x19kjcj4 xh8yej3')
                video = page_name[i].find('video', class_='x1lliihq x5yr21d xh8yej3')
                if image:
                    ad_data["media_url"] = image['src']
                elif video:
                    ad_data["media_url1"] = video['src']
                print("Optimized:", Optimized, type(Optimized))

                if not any(ad["href_link"] == ad_data["href_link"] for ad in data):
                    data.append(ad_data)

            except Exception as e:
                
                print('\n', e)
                 
        data_dict = {
            'ad_data': data,
            'first_link': first_link,
            'user': str(request.user)
        }
        return JsonResponse(data_dict)

    return render(request, 'FacebookFree.html', {'ad_data': data, 'first_link': first_link} )

