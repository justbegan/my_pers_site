from django.http.response import JsonResponse
from django.shortcuts import render, redirect
import csv
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from main_app.models import Progress_bar
from rest_framework.views import APIView
from rest_framework.response import Response
from main_app.serializers import Main_app_serializers
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main_app import urls



class SendEmail:

    API = ""
    API_URL = ""
    DOMAIN = ""
    TEXT = "Привет! \n Поздравляем тебя с прохождением марафона, выполнением всех домашних заданий и получением международного сертификата  WCHPO, 10 часов. \n С уважением, команда школы. "
    SUBJECT = "Сертификат за прохождение марафона"


    def send_simple_message(self, temp, mail):
        file_from_temp = ('STOR Obama.jpg', temp.getvalue())
        return requests.post(self.API_URL,
            auth=("api", self.API),
            files =[("attachment", file_from_temp)],
            data={"from": "Excited User <mailgun@"+ self.DOMAIN +">",
                "to": [mail, self.DOMAIN],
                "subject": self.SUBJECT,
                "text": self.TEXT,
                
                })

class CreateImage(SendEmail):
    # Стандартная длина имени участника 
    STANDART_NAME_LENGTH = 12


    def __init__(self, f_name, s_name, mail):
        self.f_name = f_name
        self.s_name = s_name
        self.mail = mail
        

    def text_position_calc(self):
        length = len(self.f_name) + len(self.s_name) - self.STANDART_NAME_LENGTH
        return length * 10
        
    def create_img(self):
        pers_name = self.f_name + " " + self.s_name
        W, H = (2480 - self.text_position_calc(), 1750)
        im = Image.open("certificate-template.jpg")
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(pers_name)
        font = ImageFont.truetype("arial.ttf", size=80)
        draw.text(((W-w)/2,(H-h)/2), pers_name,font=font, fill="#353535")
        temp = BytesIO()
        im.save(temp, format = "png")

        #функия отправки
        self.send_simple_message(temp, self.mail)
    
  


def validator(row):
    if " " in row[0] or " " in row[1] or " " in row[2]:
        return False

    if "_" in row[0] or "_" in row[1]:
        return False

    if row[0][0].isupper() == False or row[1][0].isupper() == False:
        return False

    if "." not in row[2]:
        return False

    return True


class Get_progress_bar_value(APIView):
    def get(self, request):
        messege = Progress_bar.objects.all().order_by('-id')[0] 
        serializers = Main_app_serializers(messege)
        return Response(serializers.data)

        
#Main point
@login_required(login_url='login/')
def import_csv(request):
    
    if request.method == 'POST':

        file = request.FILES['file']
        decoded_file = file.read().decode('utf-8').splitlines()
        row_num = 1
        valid_rows = {}
        
        for line in decoded_file:

            row = line.split(",")
            if not validator(row) or row in valid_rows.values():
                return JsonResponse({'row':row_num})
            valid_rows[str(row_num)] = (row)


            row_num = row_num + 1
        bar = Progress_bar(all= len(valid_rows))
        bar.save()
       
        loop = 1
        for i in valid_rows:
           

            bar_2 = Progress_bar.objects.all().last()
            bar_2.current = loop
            bar_2.save()
            p = CreateImage(valid_rows[i][0], valid_rows[i][1], valid_rows[i][2])
            p.create_img()
            loop = loop + 1

        return JsonResponse({'success':True, 'row_count':len(valid_rows)})


    return render(request, "index.html",{'test':"test"})



#Аутентификация пользователя

def loginPage(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request,username= username,password = password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Username or passwrod in incorrect')

    contex ={}
    return render(request,'login_form.html',contex)

def logOutUser(request):

    logout(request)
    return redirect('/')
