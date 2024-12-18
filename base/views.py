from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User
from django.contrib import messages
from .models import*
from django.db.models import F


def home(request):
    return render(request,'home.html')
# Register a User (Candidate or Admin)
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_role = request.POST.get('role')  # Get role (admin or candidate)

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("register_user")

        # Password validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register_user')
        
         # Validate role
        if user_role not in ['admin', 'candidate']:
            messages.error(request, "Invalid role specified.")
            return redirect('register_user')

        # Create User based on role selection
        if user_role == 'admin':
            user = User.objects.create_user(username=username, email=email, password=password, is_admin=True)
        else:
            user = User.objects.create_user(username=username, email=email, password=password, is_candidate=True)

        user.is_active = False  # Inactive until email is verified
        user.save()
        
        profile = Profile(user=user)  # Create a Profile linked to the user
        profile.save()  # Save the profile

        # Send verification email
        token = get_random_string(32)
        user.profile.token = token
        user.profile.save()
        
            # Send verification email with custom content
        send_mail(
            'Email Verification !!',
            f"""
            Hi {user.username},

            Welcome to Projectfolio! We are excited to have you join our platform. 
            Please verify your email address by clicking the link below:

            http://127.0.0.1:8000/verify/{token}/

            This will activate your account, and you'll be able to start exploring our platform.

            If you did not sign up for this account, please disregard this email.

            """,
            'annanyatiwary4@gmail.com',  # Use a dedicated support email instead of 'admin'
            [email],
        )

        
        messages.success(request, "Account created. Please verify your email.")
        return redirect('login')

    return render(request, 'register.html')


# Email Verification
def verify_email(request, token):
    try:
        user = User.objects.get(profile__token=token)
        user.is_active = True
        user.is_verified = True
        user.profile.token = None
        user.save()
        messages.success(request, "Email verified successfully!")
        return redirect('login')
    except User.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect('login')

# Login

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Custom authenticate method for email
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password):
            if not user.is_verified:
                messages.error(request, "Please verify your email first.")
                return redirect('login')

            login(request, user)
            if user.is_admin:
                return redirect('admin_dashboard')  # Admin dashboard
            elif user.is_candidate:
                return redirect('candidate_dashboard')  # Candidate dashboard
            else:
                return redirect('login')  # In case no role is assigned

        messages.error(request, "Invalid credentials.")
        return redirect('login')
    else:
        return render(request, 'login.html')



# Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# Forgot Password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = get_object_or_404(User, email=email)

            # Generate reset token
            token = get_random_string(32)
            user.profile.token = token
            user.profile.save()

            # Send reset email
            send_mail(
                'Reset Your Password',
                f"Reset your password: http://127.0.0.1:8000/reset-password/{token}/",
                'annanyatiwary4@gmail.com',
                [email],
            )
            messages.success(request, "Password reset email sent.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Email not found.")
            return redirect('forgot_password')
    return render(request, 'forgotpassword.html')

# Reset Password
def reset_password(request, token):
    try:
        user = User.objects.get(profile__token=token)
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
                return redirect(f'/reset-password/{token}/')

            user.set_password(password)
            user.profile.token = None
            user.save()
            messages.success(request, "Password reset successful!")
            return redirect('login')

        return render(request, 'reset.html', {'token': token})

    except User.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect('login')



@login_required(login_url='/login/') 

def admin_dashboard(request):
    projects = Project.objects.all()

    # Calculate progress for each project
    for project in projects:
        total_tasks = project.total_tasks
        # Correctly access the assignments related to this project
        completed_tasks = sum([assignment.completed_tasks for assignment in project.assignments.all()])
        project.progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks else 0

    return render(request, 'admin_dashboard.html', {
        'projects': projects,
    })


@login_required(login_url='/login/') 
def candidate_dashboard(request):
    # Your logic to show the candidate dashboard
    return render(request, 'candidate.html')

# View for adding a project
@login_required
def add_project(request):
    if request.method == 'POST':
        project_title = request.POST.get('title', '').strip()
        project_description = request.POST.get('description', '').strip()

        if project_title and project_description:  # Ensure both fields are provided
            Project.objects.create(title=project_title, description=project_description)
            messages.success(request, 'Project successfully added!')  # Add success message
            return redirect('admin_dashboard')  # Redirect to the dashboard after adding a project
        else:
            messages.error(request, 'Both title and description are required!')  # Error message for validation failure

    return redirect('add_project') 


# View for updating a project
@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project_title = request.POST.get('title', '').strip()
        project_description = request.POST.get('description', '').strip()

        if project_title and project_description:
            project.title = project_title
            project.description = project_description
            project.save()  # Save updated project
            messages.success(request, 'Project updated successfully!')
            return redirect('admin_dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, 'Both title and description are required!')  # Validation error message

    # Render the admin dashboard with the update modal
    return render(request, 'admin_dashboard.html', {'project': project})


# View for assigning a project to a candidate
@login_required
def assign_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        candidate_id = request.POST.get("candidate_id")
        candidate = get_object_or_404(User, id=candidate_id)

        # Create an assignment record
        Assignment.objects.create(project=project, user=candidate)

        # Send an email invitation
        send_mail(
            subject=f"You've been invited to the project '{project.title}'",
            message=f"Hello {candidate.username},\n\nYou have been invited to participate in the project '{project.title}'. Please log in to your account to see the project.",
            from_email="annanyatiwary4@gmail.com",
            recipient_list=[candidate.email],
            fail_silently=False,
        )

        messages.success(request, f"Invitation sent to {candidate.username} for project '{project.title}'.")
        return redirect("assign_project", project_id=project.id)

    candidates = User.objects.filter(is_candidate=True)  # Fetch all candidates
    return render(request, "assign.html", {"project": project, "candidates": candidates})

# View for deleting a project
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        project.delete()  # Delete the project
        messages.success(request, 'Project deleted successfully!')
        return redirect('admin_dashboard')

    return render(request, 'delete_project.html', {'project': project})

@login_required
def get_candidates(request, project_id):
    project = get_object_or_404(Project, id=project_id)  # Fetch the project
    candidates = User.objects.filter(is_candidate=True)  # Filter candidates if needed

    # Render the candidates in the template
    return render(request, 'assign.html', {'project': project, 'candidates': candidates})


from django.http import HttpResponse



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# View for admin to see candidate's score and progress for a specific project
def view_candidate_progress(request, project_id, candidate_id):
    # Get the project and candidate objects
    project = get_object_or_404(Project, id=project_id)
    candidate = get_object_or_404(User, id=candidate_id)

    # Get the assignment for this candidate and project
    assignment = Assignment.objects.filter(project=project, user=candidate).first()

    if not assignment:
        return render(request, 'error_page.html', {'message': 'No assignment found for this candidate on the project'})

    # Calculate candidate's progress (you can customize the logic)
    completed_tasks = assignment.completed_tasks
    total_tasks = project.total_tasks
    progress = (completed_tasks / total_tasks) * 100 if total_tasks else 0
    score = assignment.score  # This is a calculated field

    # Render the template with the assignment details
    return render(request, 'admin/candidate_progress.html', {
        'project': project,
        'candidate': candidate,
        'progress': progress,
        'score': score,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
    })

# Function to download the score as a PDF
def download_score_pdf(request, project_id, candidate_id):
    project = get_object_or_404(Project, id=project_id)
    candidate = get_object_or_404(User, id=candidate_id)
    assignment = Assignment.objects.filter(project=project, user=candidate).first()

    if not assignment:
        return HttpResponse("No assignment found", status=404)

    completed_tasks = assignment.completed_tasks
    total_tasks = project.total_tasks
    score = assignment.score
    progress = (completed_tasks / total_tasks) * 100 if total_tasks else 0

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="score_{candidate.username}_{project.title}.pdf"'

    # Create PDF document
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Candidate: {candidate.username}")
    p.drawString(100, 730, f"Project: {project.title}")
    p.drawString(100, 710, f"Completed Tasks: {completed_tasks} / {total_tasks}")
    p.drawString(100, 690, f"Progress: {progress:.2f}%")
    p.drawString(100, 670, f"Score: {score:.2f}%")
    p.showPage()
    p.save()

    return response

# Function to send the score via email
def send_score_email(request, project_id, candidate_id):
    project = get_object_or_404(Project, id=project_id)
    candidate = get_object_or_404(User, id=candidate_id)
    assignment = Assignment.objects.filter(project=project, user=candidate).first()

    if not assignment:
        return HttpResponse("No assignment found", status=404)

    completed_tasks = assignment.completed_tasks
    total_tasks = project.total_tasks
    score = assignment.score
    progress = (completed_tasks / total_tasks) * 100 if total_tasks else 0

    # Prepare the email content
    subject = f"Your Progress and Score for {project.title}"
    message = f"""
    Dear {candidate.username},
    
    Here is your progress and score for the project: {project.title}.
    
    Completed Tasks: {completed_tasks} / {total_tasks}
    Progress: {progress:.2f}%
    Score: {score:.2f}%
    
    Regards,
    Your Project Management Team
    """

    # Send the email
    send_mail(
        subject,
        message,
        'annanyatiwary4@gmail.com',  # Replace with your admin email
        [candidate.email],
        fail_silently=False,
    )

    return HttpResponse("Score sent to the candidate successfully!", status=200)

###############CANDIDATE VIEWS LOGIC################

@login_required
def candidate_dashboard(request):
    user = request.user

    # Get all projects assigned to the user
    assignments = Assignment.objects.filter(user=user)
    projects = [assignment.project for assignment in assignments]

    # Calculate the overall progress for the candidate
    total_projects = assignments.count()
    completed_projects = assignments.filter(project__completed_tasks=F('project__total_tasks')).count()
    remaining_projects = total_projects - completed_projects

    # Calculate score as a percentage (avoid division by zero)
    score = 0
    if total_projects > 0:
        score = (completed_projects / total_projects) * 100

    overall_progress = {
        'total_projects': total_projects,
        'completed_projects': completed_projects,
        'remaining_projects': remaining_projects,
        'score': score  # You can calculate a score here if needed
    }
    
    stroke_dashoffset = 314.16 - (314.16 * overall_progress['score'] / 100)

    return render(request, 'candidate.html', {
        'projects': projects,
        'overall_progress': overall_progress,
        'stroke_dashoffset': stroke_dashoffset
    })

@login_required
def project_progress(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    # Calculate the progress of the project
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    remaining_tasks = total_tasks - completed_tasks - in_progress_tasks

    project_progress = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'remaining_tasks': remaining_tasks,
    }

    # Calculate stroke dash offset for each progress circle
    completed_progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    in_progress_progress = (in_progress_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    remaining_progress = 100 - completed_progress - in_progress_progress

    # Stroke dash offset calculations for circles (314.16 is the circumference of a circle with radius 50)
    completed_offset = 314.16 - (314.16 * completed_progress / 100)
    in_progress_offset = 314.16 - (314.16 * in_progress_progress / 100)
    remaining_offset = 314.16 - (314.16 * remaining_progress / 100)

    return render(request, 'project_progress.html', {
        'project': project,
        'project_progress': project_progress,
        'tasks': tasks,
        'completed_offset': completed_offset,
        'in_progress_offset': in_progress_offset,
        'remaining_offset': remaining_offset,
    })

@login_required
def mark_project_completed(request, project_id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=project_id)

        # Toggle the completion status
        if project.completed_tasks == project.total_tasks:
            project.completed_tasks = 0  # Unmark completion
        else:
            project.completed_tasks = project.total_tasks  # Mark as completed

        project.save()

    return redirect('candidate_dashboard')  # Redirect to refresh the progress




@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(project=project, title=title, description=description)
        
        # Update the project tasks count
        project.total_tasks += 1
        project.remaining_tasks += 1
        project.save()

        return redirect('candidate_dashboard')  # Redirect back to dashboard

    return render(request, 'add_task.html', {'project': project})




from django.core.exceptions import ObjectDoesNotExist


@login_required
@login_required
def profile_settings(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # If the user does not have a profile, create one
        profile = Profile(user=request.user)
        profile.save()

    if request.method == 'POST':
        # Manually update the profile data
        bio = request.POST.get('bio', profile.bio)
        profile_picture = request.FILES.get('profile_picture', profile.profile_picture)

        profile.bio = bio
        profile.profile_picture = profile_picture

        profile.save()

        # Show a success message
        messages.success(request, 'Your profile has been updated successfully!')

        # Redirect to the respective dashboard (Admin or Candidate)
        if request.user.is_admin:  # Assuming `is_staff` indicates admin user
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            return redirect('candidate_dashboard')  # Redirect to candidate dashboard

    return render(request, 'profile_settings.html', {'profile': profile})
