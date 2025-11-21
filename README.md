# 🎓 Exam Management System

A comprehensive Django-based web application for managing exams, student registrations, and results with a modern, user-friendly interface.

## ✨ Features

### 🔐 **Dual Authentication System**
- **Examiner Registration/Login**: Separate authentication for exam creators
- **Student Registration/Login**: Dedicated student portal
- **Role-based Access Control**: Secure access based on user roles
- **Profile Management**: Auto-fill forms with saved profile data

### 👨‍🏫 **Examiner Workflow**
1. **Create Exam** (`/examiner/create-exam/`)
   - Set exam title, description, and unique exam code
   - Configure duration and registration/exam dates
   - Auto-fill examiner information from profile

2. **Set Exam Details** (`/examiner/exam-details/<exam_id>/`)
   - Add detailed instructions for students
   - Specify difficulty level and topics
   - Manage question types (MCQ, Short Answer, Drag-Drop)

3. **Manage Exam** (`/examiner/manage-exam/<exam_id>/`)
   - View and verify student registrations
   - Invalidate registrations with reasons
   - Track participation and results
   - Handle student requests and inquiries

### 🎓 **Student Workflow**
1. **Home Dashboard** (`/candidate/home/`)
   - View announcements and tips
   - See upcoming registered exams
   - Quick access to exam browsing

2. **Browse & Register** (`/candidate/exams/`)
   - View all available exams
   - Register with exam code verification
   - Auto-fill registration from profile

3. **Registration Process**
   - **Confirmation** (`/candidate/exams/confirmation/<exam_id>/`)
     - PDF preview of registration form
     - Print registration documents
   - **Instructions** (`/candidate/exams/instructions/<exam_id>/`)
     - View exam details and instructions
     - Check registration status

4. **Exam Taking** (`/candidate/exams/take/<exam_id>/`)
   - Interactive exam interface
   - Real-time timer and progress tracking
   - Multiple question types support

5. **Results & Requests**
   - View exam results with detailed breakdown
   - Submit inquiries and requests
   - Print result sheets

### 📊 **Advanced Features**
- **Registration Verification System**
  - Pending Verification → Ready for Exam → Invalid
  - Reason tracking for invalidated registrations
  - Automatic student notifications

- **Messaging System**
  - Student requests and inquiries
  - Examiner replies with templates
  - Request status tracking

- **PDF Generation**
  - Professional registration forms
  - Detailed result sheets
  - Exam results reports for examiners

- **Question Management**
  - Multiple Choice Questions (MCQ)
  - Short Answer Questions
  - Drag & Drop Questions
  - Auto-generated question numbering

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8+
- Django 5.2.6
- SQLite (included with Python)

### Installation

1. **Clone/Download the project**
   ```bash
   cd exam_management_system
   ```

2. **Install dependencies**
   ```bash
   pip install django
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open browser to `http://127.0.0.1:8000/`
   - Create examiner or student accounts
   - Start using the system!

## 📁 **Project Structure**

```
exam_management_system/
├── exam_system/           # Main Django project
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── users/                # User authentication app
│   ├── models.py        # User profile models
│   ├── views.py         # Authentication views
│   ├── forms.py         # Registration forms
│   └── urls.py          # User URLs
├── exams/                # Exam management app
│   ├── models.py        # Exam, Question, Registration models
│   ├── views.py         # Exam workflow views
│   ├── forms.py         # Exam forms
│   └── urls.py          # Exam URLs
├── messaging/            # Communication app
│   ├── models.py        # Message and Request models
│   ├── views.py         # Messaging views
│   └── urls.py          # Messaging URLs
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── home.html        # Landing page
│   ├── users/           # Authentication templates
│   ├── exams/           # Exam-related templates
│   └── messaging/       # Messaging templates
├── static/               # Static files
│   └── css/
│       └── style.css    # Custom CSS
└── manage.py            # Django management script
```

## 🎨 **UI/UX Features**

- **Modern Design**: Bootstrap 5 with custom styling
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Professional Color Scheme**: Blue for examiners, green for students
- **Font Awesome Icons**: Enhanced visual appeal
- **Interactive Elements**: Hover effects, animations, and transitions
- **Print-Optimized**: Professional PDF-ready templates

## 🔧 **Technical Details**

### **Database Models**
- **Profile**: Extended user profiles with role-specific fields
- **Exam**: Comprehensive exam information with examiner details
- **Question**: Support for multiple question types
- **Registration**: Detailed student registration with status tracking
- **Result**: Exam results with answer tracking
- **Request**: Student-instructor communication system

### **URL Structure**
```
# Examiner URLs
/examiner/signup/                    # Examiner registration
/examiner/login/                     # Examiner login
/examiner/profile/                   # Examiner profile
/examiner/create-exam/               # Create new exam
/examiner/exam-details/<id>/         # Set exam details
/examiner/manage-exam/<id>/          # Manage exam
/examiner/manage-exam/<id>/requests/ # View requests
/examiner/request/<id>/reply/        # Reply to request

# Student URLs
/candidate/signup/                   # Student registration
/candidate/login/                    # Student login
/candidate/profile/                  # Student profile
/candidate/home/                     # Student dashboard
/candidate/exams/                    # Browse exams
/candidate/exams/register/<id>/      # Register for exam
/candidate/exams/confirmation/<id>/  # Registration confirmation
/candidate/exams/instructions/<id>/  # Exam instructions
/candidate/exams/take/<id>/          # Take exam
/candidate/exams/results/<id>/       # View results
/candidate/requests/                 # Student requests
```

### **Key Features**
- **Exam Code Validation**: Secure registration with unique codes
- **Profile Auto-fill**: Seamless form completion
- **Status Tracking**: Complete registration workflow
- **PDF Generation**: Professional document printing
- **Real-time Updates**: Live progress tracking
- **Mobile Responsive**: Works on all devices

## 🎯 **Usage Examples**

### **For Examiners**
1. Register as an examiner
2. Create an exam with unique code
3. Add questions (MCQ, Short Answer, Drag-Drop)
4. Set exam details and instructions
5. Verify student registrations
6. Monitor exam participation
7. View and print results

### **For Students**
1. Register as a student
2. Browse available exams
3. Register with exam code
4. View registration confirmation
5. Read exam instructions
6. Take the exam
7. View results and print certificates

## 🔒 **Security Features**

- **Role-based Access Control**: Users can only access their designated areas
- **Exam Code Validation**: Prevents unauthorized registrations
- **CSRF Protection**: Django's built-in security
- **Input Validation**: Comprehensive form validation
- **Secure Authentication**: Django's authentication system

## 📱 **Browser Support**

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 **Deployment**

For production deployment:

1. **Configure Settings**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set up proper database (PostgreSQL recommended)

2. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Environment Variables**
   - Set `SECRET_KEY`
   - Configure database credentials
   - Set up email settings

4. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure Nginx or Apache
   - Set up SSL certificates

## 📞 **Support**

For technical support or feature requests, please contact the development team.

## 📄 **License**

This project is developed for educational and institutional use.

---

**🎉 The Exam Management System is now complete and ready for use!**

Access the system at `http://127.0.0.1:8000/` and start managing exams efficiently with this comprehensive solution.
