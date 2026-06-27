<!-- 1. Update the navbar for the auth user to add pages links. Dashboard, TimeTable, Profile -->
<!-- 2. Make the auth pages responsive -->
<!-- 3. desing all remaining timetable all pages, profile all pags, etc -->
<!-- 6. New pages like timetable pages are not responsive check that  -->
<!-- 7. Make the footer correct and same for each page  -->
<!-- 8. Make the Dashboard Page responsive  -->
<!-- 4. Add the direct link to auth pages on register all buttons -->
<!-- 9. Make the Add task, Add note back to its list page instead of dashboard page.  -->
<!-- 10. Make the logic correct while adding any task or notes from specific subject notes it should not ask the subject as this make it worse in term of logic and also show subject selection field if it is showed without the subject page  -->
<!-- 11. Complete all the logics features functionality code as soon as possible -->
5. Add the notification reminder functionality because it is the core feature in our app
7. Add the date field in form pages not text it is difficult to add the deadline date data
6. Integrity Error: Unique constraint failed show error improper , error should be display in erro tag not on web crashing etc:
```bash
IntegrityError at /subjects/add-new-subject/
UNIQUE constraint failed: academy_subject.user_id, academy_subject.name
Request Method:	POST
Request URL:	https://studymate.pythonanywhere.com/subjects/add-new-subject/
Django Version:	5.2.7
Exception Type:	IntegrityError
Exception Value:	
UNIQUE constraint failed: academy_subject.user_id, academy_subject.name
Exception Location:	/home/studymate/University-Project/myenv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py, line 360, in execute
Raised during:	academy.views.add_or_update__subject
Python Executable:	/usr/local/bin/uwsgi
Python Version:	3.12.8
Python Path:	
['/home/studymate/University-Project/academy_tracker',
 '/var/www',
 '.',
 '',
 '/var/www',
 '/usr/local/lib/python312.zip',
 '/usr/local/lib/python3.12',
 '/usr/local/lib/python3.12/lib-dynload',
 '/home/studymate/University-Project/myenv/lib/python3.12/site-packages']
Server time:	Thu, 23 Apr 2026 21:41:51 +0000
```

