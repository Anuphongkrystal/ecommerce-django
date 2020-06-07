#Handbook

#Step
[+] mkvirtualenv ecommerce <bt>
[+] pip install django <br>
[+] workon ecommerce <br>
[+] django-admin startproject ecommerce <br>
[+] python manage.py runserver <br>
[+] pytohn manage.py startapp store <br>
[+] pip install Pillow <br>
[+] python manage.py makemigrations <br>
[+] python manage.py migrate <br>
[+] python manage.py createsuperuser<br>
[+] pip install django-crispy-forms <br>
[+] pip install stripe <br>
//ถ้ามีหลาย App ต้องระบุชื่อ App ด้วย
[+] python manage.py makemigrations store<br>
//เพื่อไม่ให้เกิดผลกระทบตอนที่ เปลี่ยนแปลงmodel
[+] python manage.py migrate --fake store<br>
