import json
from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.utils import timezone

from .models import ShortURL, ClickAnalytics
from .utils import generate_shortcode, get_location_from_ip

import string, random

def create_short_url(request):
    data = json.loads(request.body)
    url = data.get("url")
    shortcode = data.get("shortcode") or generate_shortcode()
    validity= int(data.get("validity", 30))

    expiry = timezone.now() + timedelta(minutes=validity)

    if ShortURL.objects.filter(shortcode=shortcode).exists():
        return JsonResponse({"error": "Shortcode already exists."}, status=409)

    short = ShortURL.objects.create(
        shortcode=shortcode,
        original_url =url,
        expires_at=expiry
    )
    return JsonResponse({
        "shortLink": f"http://localhost:8000/{shortcode}",
        "expiry": short.expires_at.isoformat()
    }, status=201)



def redirect_view(request, shortcode):
    try:
        short =ShortURL.objects.get(shortcode=shortcode)
        if timezone.now() > short.expires_at:
            return JsonResponse({"error": "Link expired"}, status=410)

        # Update analytics
        short.click_count += 1
        short.save()

        ref= request.META.get("HTTP_REFERER", "")
        ip =request.META.get("REMOTE_ADDR", "")
        loc =get_location_from_ip(ip)

        ClickAnalytics.objects.create(
            short_url=short,
            referrer=ref,
            location=loc
        )
        return redirect(short.original_url)

    except ShortURL.DoesNotExist:
        return JsonResponse({"error": "Invalid shortcode"}, status=404)


def get_stats(request, shortcode):
    try:
        short = ShortURL.objects.get(shortcode=shortcode)
        analytics = ClickAnalytics.objects.filter(short_url=short)

        return JsonResponse({
            "original_url": short.original_url,
            "created_at": short.created_at.isoformat(),
            "expires_at": short.expires_at.isoformat(),
            "clicks": short.click_count,
            "click_data": [{
                "timestamp": a.timestamp.isoformat(),
                "referrer": a.referrer,
                "location": a.location
            } for a in analytics]
        })

    except ShortURL.DoesNotExist:
        return JsonResponse({"error": "Shortcode not found"}, status=404)




def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def home(request):
    if request.method== 'POST':
        url = request.POST.get('url')
        shortcode = request.POST.get('shortcode') or generate_shortcode()
        validity = int(request.POST.get('validity', 60))


        short_url = ShortURL.objects.create(
        original_url=url,
        shortcode=shortcode,
        expires_at=timezone.now() + timezone.timedelta(minutes=validity)
    )

        full_short_url = request.build_absolute_uri(f'/{shortcode}')
        return render(request,'shortner/home.html',{'short_url':full_short_url})
    
    return render(request,'shortner/home.html')
