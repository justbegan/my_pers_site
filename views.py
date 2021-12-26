from django.shortcuts import render, HttpResponse
import csv
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


class CreateImage:
    # Стандартная длина имени участника 
    standart_name_length = 12
    TEXT = "Привет! \n Поздравляем тебя с прохождением марафона, выполнением всех домашних заданий и получением международного сертификата  WCHPO, 10 часов. \n С уважением, команда школы. "
    SUBJECT = "Сертификат за прохождение марафона"


    def __init__(self, f_name, s_name):
        self.f_name = f_name
        self.s_name = s_name
        

    def meter(self):
        length = len(self.f_name) + len(self.s_name) - self.standart_name_length
        return length * 10
        
    def create_img(self):
        person_name = self.f_name + " " + self.s_name
        W, H = (2480 - self.meter() ,1750)
        msg = person_name
        im = Image.open("certificate-template.jpg")
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(msg)
        font = ImageFont.truetype("arial.ttf", size=80)
        draw.text(((W-w)/2,(H-h)/2), msg,font=font, fill="#353535")


        # img_name = person_name + "_cert.jpg"
        # im.save(img_name, "PNG")
        # 

        temp = BytesIO()
        im.save(temp, format = "png")
        self.send_simple_message(temp)
    
    def send_simple_message(self, temp):
        f = ('STOR Obama.jpg', temp.getvalue())
        #f = open(file_name, 'rb')
        return requests.post(
            "https://api.mailgun.net/v3/sandboxd68aac39f74b47cdaee0a136b31c499f.mailgun.org/messages",
            auth=("api", "00a9dfbf3e6afce1385b659a31d2fb51-1831c31e-25182258"),
            files =[("attachment", f)],
            data={"from": "Excited User <mailgun@sandboxd68aac39f74b47cdaee0a136b31c499f.mailgun.org>",
                "to": ["justbegan@mail.ru", "sandboxd68aac39f74b47cdaee0a136b31c499f.mailgun.org"],
                "subject": self.SUBJECT,
                "text": self.TEXT,
                
                })


def validator(row):
    if " " in row[0] or " " in row[1] or " " in row[2]:
        print("1")
        return False

    if "_" in row[0] or "_" in row[1]:
        print("2")
        return False

    if row[0][0].isupper() == False or row[1][0].isupper() == False:
        print("3")
        return False

    if "." not in row[2]:
        print("4")
        return False

    return True






def import_csv(request):

    if request.POST:
        
        file = request.FILES['file'] 
        decoded_file = file.read().decode('utf-8').splitlines()
        row_num = 1
        a = {}
        
        for line in decoded_file:

            row = line.split(",")
            if not validator(row) or row in a.values():
                print(row)
                return render(request, "index.html",{'row':row_num})
            a[str(row_num)] = (row)



          
            row_num = row_num + 1

        for i in a:
            p = CreateImage(a[i][0], a[i][1])
            p.create_img()
        
        
            

    return HttpResponse("Uploaded")
    #return render(request, "index.html",{'test':"test"})
