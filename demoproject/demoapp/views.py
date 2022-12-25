from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ProductDetails
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .serializers import ProductDetailsSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core import serializers
import json 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Function for rendering the home level
@csrf_exempt
def index(request):
    name = request.GET.get('name')
    city = request.GET.get('city')
    print(request, ">>>>>>>", name, city)
    if request.method == "POST":
        print("Form is submitted")
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        created_date = request.POST.get('created_date')
        product_active = request.POST.get('product_active')
        product_description = request.POST.get('product_description')
        # if product_active == "on":
        #     product_active = True
        # else:
        #     product_active = False

        print(product_name, product_price, created_date, product_active)
        # ProductDetails.objects.create(product_name=product_name,
        #                             product_price= product_price,
        #                             product_active=product_active,
        #                             created_date=created_date)

        product_object = ProductDetails()
        product_object.product_name = product_name
        product_object.product_price = product_price
        product_object.product_active = product_active
        product_object.created_date = created_date
        product_object.product_description = product_description
        product_object.save()
 
        # hobbies = request.POST.getlist("hobbies")
        # print(hobbies, "###########")
        # radio_value = request.POST.get("choose")
        # print(radio_value, "@@@@@@@@@@@@@@@")


    context = {"product_data": "My second product", "product_name": "Iphone"}
    return render(request=request, template_name="index.html",
                context=context)
    # return HttpResponse("<h1>This is my first demo project</h1>")
    # print("hello")

def display_products(request):
    products_object = ProductDetails.objects.all()
    # print(str(ProductDetails.objects.all().query))
    context = {"products_object": products_object}
    return render(request, "all_products.html", context)

def delete_product(request, id):
    ProductDetails.objects.filter(id=id).delete()
    return redirect("display_products")

def product_details(request, id):
    product_details = ProductDetails.objects.get(id=id)
    context = {"product_details": product_details}
    return render(request, "product_detail.html", context)

@csrf_exempt
def update_product_detail(request):
    try:
        if request.method == "POST":
            product_name = request.POST.get('productname')
            id = request.POST.get('id')
            product_obj = ProductDetails.objects.filter(id=id).first()
            product_obj.product_name = product_name
            product_obj.save()
            print(id, product_name, "$$$$$$$$$$$$$$$$$$$$$$")
        return JsonResponse("success", safe=False)
        # return render(request,"update_product.html")
    except Exception as e:
        return JsonResponse(e, safe=False)
        # return render(request,"update_product.html")
 
@csrf_exempt
def login_user(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/display_products/')
            else:
                return HttpResponse("Username or password is invalid")
    except Exception as e:
        print(e)
    return render(request, 'login.html') 

def logout_user(request):
    logout(request)
    return redirect('/display_products/')

# class UpdateProductDetail:

#     def __init__(self, request):
#         self.request = request

#     def get_product_detail(self, request):
#         try:
#             if request.method == "POST":
#                 product_name = request.POST.get('productname')
#                 id = request.POST.get('id')
#                 product_obj = ProductDetails.objects.filter(id=id).first()
#                 product_obj.product_name = product_name
#                 product_obj.save()
#                 print(id, product_name, "$$$$$$$$$$$$$$$$$$$$$$")
#             return JsonResponse("success", safe=False)
#             # return render(request,"update_product.html")
#         except Exception as e:
#             return JsonResponse(e, safe=False)


class ProductViewset(viewsets.ViewSet):
    queryset = ProductDetails.objects.all() 
    serializer_class = ProductDetailsSerializer
    permission_classes = [IsAuthenticated]
    def list(self, request):
        # print(str(ProductDetails.objects.all().query))

        queryset = ProductDetails.objects.all()
        serializer = ProductDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        created_date = request.POST.get('created_date')
        product_active = request.POST.get('product_active')
        product_description = request.POST.get('product_description')

        product_object = ProductDetails()
        product_object.product_name = product_name
        product_object.product_price = product_price
        product_object.product_active = product_active
        product_object.created_date = created_date
        product_object.product_description = product_description
        product_object.save()
        return JsonResponse({"success": product_object}, safe=False)

    def retrieve(self, request, pk=None):
        try:
            product_obj = ProductDetails.objects.filter(id=pk)
            if product_obj:
                print(product_obj, "^^^^^^^^^^^^")
                serializer = ProductDetailsSerializer(product_obj, many=True)
                return Response(serializer.data)
            else:
                print("Inside else statement")
                message = f"search {pk} not found"
                return JsonResponse({"message": message}, safe=False)
        except Exception as e:
            message = f"Something went wrong"
            return JsonResponse({"message": message}, safe=False)

    def update(self, request, pk=None):
        try:
            if type(pk) == int:
                instance = self.queryset.get(id=pk)
                serializer = self.serializer_class(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response("Please provide a primary key")
        except:
            return Response("Please provide a primary key")

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(id=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        pass


def display_product_api(request):
    product_obj = serializers.serialize('json', ProductDetails.objects.all())
    product_result = json.loads(product_obj)
    return JsonResponse(product_result, safe=False)

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product_api(request, id):
    if request.method == "DELETE":
        id_avail = ProductDetails.objects.filter(id=id)
        if id_avail:
            ProductDetails.objects.filter(id=id).delete()
            return JsonResponse(f"Provided id: {id} is deleted", safe=False)
        else:
            return JsonResponse(f"Provided id: {id} not found", safe=False)
    else:
        return JsonResponse(f"Please provide correct method", safe=False)
        
@csrf_exempt
def login_by_api(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                tokens_rcvd = get_tokens_for_user(user)
                return JsonResponse(tokens_rcvd)
            else:
                return HttpResponse("Username or password is invalid")
    except Exception as e:
        print(e)
        return HttpResponse(e)
