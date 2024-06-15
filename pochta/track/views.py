import os

import mysql.connector
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('HOST', default='localhost'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    database=os.getenv('BASE_NAME'))
mycursor = mydb.cursor()


ITEM_PER_PAGE = 5


def index(request):
    if request.method == 'POST':
        track = request.POST.get('track')
        sql = f'INSERT INTO tracking_delivery (track) VALUES ("{track}");'
        mycursor.execute(sql)
        mydb.commit()
        return redirect('track:index')
    else:
        sql = 'SELECT * FROM tracking_delivery;'
        mycursor.execute(sql)
        track_list = mycursor.fetchall()
        paginator = Paginator(track_list, ITEM_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            'track/index.html',
            context={
                'page_obj': page_obj})
