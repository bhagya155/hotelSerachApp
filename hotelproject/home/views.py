from django.shortcuts import render
from .models import*
from django.http import JsonResponse

def home(request):
    context = {"amenities": Amenities.objects.all}
    return render(request, 'home.html', context)

def get_hotel(request):
    try:
        hotel_objs = Hotel.objects.all()

        if request.GET.get('sort_by'):
            sort_by_value = request.GET.get('sort_by')
            if sort_by_value == 'asc':
                hotel_objs = hotel_objs.order_by('hotel_price')
            elif sort_by_value == 'dsc': 
                hotel_objs = hotel_objs.order_by('-hotel_price')

        if request.GET.get('amount'):
            amount = request.GET.get('amount')
            hotel_objs = hotel_objs.filter(hotel_price__lte=amount)

        if request.GET.get('amenities'):
            amenities = request.GET.get('amenities')
            amenities = str(amenities).split(',')
            am = []
            for amenity in amenities:
                am.append(int(amenity))
            
            hotel_objs = hotel_objs.filter(amenities__in = am).distinct()

        payload = []
        for hotel_obj in hotel_objs:
            payload.append({
                            'hotel_name': hotel_obj.hotel_name,
                            'hotel_price': hotel_obj.hotel_price,
                            'hotel_description': hotel_obj.hotel_description,
                            'banner_img': '/media/' + str(hotel_obj.banner_img),
                            'amenities' : hotel_obj.get_amenities()
            })

        return JsonResponse(payload, safe=False)
    
        

    except Exception as e:
        print(e)

    return JsonResponse({'message' : "Something went wrong"})
    

# Create your views here.
