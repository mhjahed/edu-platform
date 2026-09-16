<!-- EXAM MANAGEMENT SYSTEM · indigo #818cf8 on #0d1117 · widgets verified 2026-09-12 -->

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,100:818cf8&height=190&section=header&text=EXAM%20MANAGEMENT&fontSize=54&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=dual%20portals%20%C2%B7%20exam%20codes%20%C2%B7%20timed%20exams%20%C2%B7%20pdf%20results%20%E2%80%94%20django%205.2&descSize=16&descAlignY=60" alt="Exam Management System" />

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=19&duration=2600&pause=900&color=A5B4FC&center=true&vCenter=true&width=780&height=95&lines=examiner+side+%C3%97+candidate+side;exam+code+validation+%C2%B7+real-time+timer;pdf+sheets+%C2%B7+results+%C2%B7+requests" alt="typing" />

<p>
  <img src="https://img.shields.io/badge/django-5.2.6-0d1117?style=for-the-badge&logo=django&logoColor=44b78b" alt="django" />
  <img src="https://img.shields.io/badge/python-3.8%2B-0d1117?style=for-the-badge&logo=python&logoColor=3776ab" alt="python" />
  <img src="https://img.shields.io/badge/bootstrap-5-0d1117?style=for-the-badge&logo=bootstrap&logoColor=7952b3" alt="bootstrap" />
  <img src="https://img.shields.io/badge/auth-dual%20portal-818cf8?style=for-the-badge&logoColor=white" alt="auth" />
  <img src="https://img.shields.io/badge/pdf-sheets%20%2B%20results-0d1117?style=for-the-badge&logoColor=a5b4fc" alt="pdf" />
</p>

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:818cf8,100:0d1117&height=3" alt="" />

## ▍$ cat overview.txt

A full exam operations system with **separate portals for examiners and
candidates** — from authoring an exam, through code-gated registration, to timed
sittings and printable result sheets. Role-aware routing keeps each side of the
platform in its own lane.

```yaml
portals   : examiner (create/manage/verify) · candidate (register/sit/results)
questions : mcq · short answer · drag-and-drop — auto-numbered
pipeline  : pending verification → ready for exam → invalid (with reason)
docs      : registration forms + result sheets — print-optimized pdf
comms     : request / reply messaging with status tracking
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:818cf8,100:0d1117&height=3" alt="" />

## ▍$ whoami --role

<table>
<tr>
<th width="50%">EXAMINER</th>
<th width="50%">CANDIDATE</th>
</tr>
<tr>
<td valign="top">

▸ create exam — title, code, dates, duration
▸ compose instructions + difficulty + topics
▸ add mcq / short / drag-drop questions
▸ verify or invalidate registrations (with reason)
▸ track participation, handle requests
▸ print full exam result reports

</td>
<td valign="top">

▸ home dashboard — announcements, tips
▸ browse exams · register with **exam code**
▸ pdf-preview + print registration form
▸ read instructions before the clock starts
▸ sit exam — live timer + progress tracking
▸ view results, submit inquiries, print sheet

</td>
</tr>
</table>

```diff
registration guard:  code wrong → rejected · pending → verified → ready
                     examiner invalidates → reason logged → student notified
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:818cf8,100:0d1117&height=3" alt="" />

## ▍$ ./setup

```bash
git clone https://github.com/mhjahed/exam-management.git && cd exam-management
pip install django
python manage.py migrate
python manage.py createsuperuser        # optional — admin panel
python manage.py runserver              # → http://127.0.0.1:8000/
```

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:818cf8,100:0d1117&height=3" alt="" />

## ▍$ grep -E "^(GET|POST)" routes.map — condensed

| SIDE | ROUTE | PURPOSE |
|---|---|---|
| examiner | `/examiner/signup/` · `/login/` · `/profile/` | auth + auto-fill profile |
| examiner | `/examiner/create-exam/` | new exam + code |
| examiner | `/examiner/exam-details/<id>/` | instructions + question set |
| examiner | `/examiner/manage-exam/<id>/` · `/requests/` · `/request/<id>/reply/` | verification + comms |
| candidate | `/candidate/home/` · `/exams/` | dashboard + catalogue |
| candidate | `/candidate/exams/register/<id>/` · `/confirmation/<id>/` · `/instructions/<id>/` | registration pipeline |
| candidate | `/candidate/exams/take/<id>/` · `/results/<id>/` | the sitting + outcome |
| candidate | `/candidate/requests/` | inquiries + replies |

## ▍$ tree .

```
exam_management_system/
├── exam_system/     settings · urls · wsgi
├── users/           profiles · dual auth
├── exams/           exam · question · registration · result models
├── messaging/       request / reply system
├── templates/       base · users · exams · messaging
├── static/css/
└── manage.py
```

**security** — rbac routing · exam-code validation · csrf tokens · full form validation · django auth
**ui** — bootstrap 5 · examiner blue / student green schemes · font awesome · print-optimized

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:818cf8,100:0d1117&height=3" alt="" />

## ▍$ cat deploy.notes

```bash
# production checklist
DEBUG=False                # settings.py
ALLOWED_HOSTS=[...]        # your domain
python manage.py collectstatic
# postgres recommended · gunicorn + nginx · ssl via certbot
```

<br/>

<div align="center">

`built end-to-end by` **[MH JAHED](https://github.com/mhjahed)** · sylhet, bangladesh · `mhjahed@proton.me`

</div>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:818cf8,100:0d1117&height=110&section=footer" alt="" />
