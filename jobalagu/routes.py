import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, send_from_directory, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_

from app import app, db, mail
from flask_mail import Message
from models import User, Job, Application
from forms import LoginForm, RegisterForm, JobForm, ApplicationForm, ApplicationStatusForm, JobSearchForm
from utils import admin_required
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_mail import Message
from app import app, mail
from flask import render_template, request
from flask_babel import _
from flask_mail import Message
from flask import current_app

from flask import render_template, request

@app.route('/resume', methods=['GET'])
def resume_form():
    return render_template('resume_form.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    objective = request.form.get('objective')
    skills = request.form.get('skills')
    education = request.form.get('education')
    experience = request.form.get('experience')
    projects = request.form.get('projects')
    certifications = request.form.get('certifications')
    languages = request.form.get('languages')
    hobbies = request.form.get('hobbies')
    references = request.form.get('references')

    return render_template(
        'resume_view.html',
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        objective=objective,
        skills=skills,
        education=education,
        experience=experience,
        projects=projects,
        certifications=certifications,
        languages=languages,
        hobbies=hobbies,
        references=references
    )


@app.route('/admin/send-email', methods=['GET', 'POST'])
@login_required
def send_email():
    if request.method == 'POST':
        recipient = request.form.get('recipient')
        subject = request.form.get('subject')
        body = request.form.get('body')
        if recipient and subject and body:
            try:
                msg = Message(subject=subject,
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[recipient],
                              body=body)
                mail.send(msg)
                flash('Email sent successfully!', 'success')
            except Exception as e:
                app.logger.error(f"Failed to send email: {e}")
                flash('Failed to send email.', 'danger')
        else:
            flash('All fields are required.', 'warning')
    return render_template('send_email.html')

@app.route('/')
def index():
    # Get recent jobs for homepage
    recent_jobs = Job.query.filter_by(is_active=True).order_by(Job.posted_at.desc()).limit(6).all()
    job_count = Job.query.filter_by(is_active=True).count()
    company_count = db.session.query(Job.company).distinct().count()
    
    return render_template('index.html', 
                         recent_jobs=recent_jobs,
                         job_count=job_count,
                         company_count=company_count)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.full_name}!', 'success')

            # ✅ Send email to admin after successful login
            try:
                msg = Message(subject='New User Login - Job Portal',
                              sender=current_app.config['MAIL_USERNAME'],
                              recipients=['alagujothi.alagapuri@gmail.com'])  # Change to actual admin email
                msg.body = f"The user '{user.full_name}' ({user.email}) has just logged in."
                mail.send(msg)
            except Exception as e:
                print(f"[ERROR] Failed to send login notification email: {e}")

            # Redirect based on user role
            if user.is_admin:
                return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
            else:
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            location=form.location.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get user's recent applications
    recent_applications = Application.query.filter_by(user_id=current_user.id)\
                                         .order_by(Application.applied_at.desc())\
                                         .limit(5).all()
    
    # Get application statistics
    total_applications = Application.query.filter_by(user_id=current_user.id).count()
    pending_applications = Application.query.filter_by(user_id=current_user.id, status='pending').count()
    accepted_applications = Application.query.filter_by(user_id=current_user.id, status='accepted').count()
    
    return render_template('dashboard.html',
                         recent_applications=recent_applications,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         accepted_applications=accepted_applications)

@app.route('/jobs')
def jobs():
    form = JobSearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Build query based on search parameters
    query = Job.query.filter_by(is_active=True)
    
    search_term = request.args.get('search_term', '')
    location_filter = request.args.get('location', '')
    job_type_filter = request.args.get('job_type', '')
    
    if search_term:
        query = query.filter(or_(
            Job.title.ilike(f'%{search_term}%'),
            Job.company.ilike(f'%{search_term}%'),
            Job.description.ilike(f'%{search_term}%')
        ))
    
    if location_filter:
        query = query.filter(Job.location.ilike(f'%{location_filter}%'))
    
    if job_type_filter:
        query = query.filter(Job.job_type == job_type_filter)
    
    jobs_pagination = query.order_by(Job.posted_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Pre-populate form with current search values
    form.search_term.data = search_term
    form.location.data = location_filter
    form.job_type.data = job_type_filter
    
    return render_template('jobs.html', 
                         jobs=jobs_pagination.items,
                         pagination=jobs_pagination,
                         form=form)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    has_applied = False
    user_application = None
    if current_user.is_authenticated and not current_user.is_admin:
        user_application = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first()
        has_applied = user_application is not None
    
    return render_template('job_detail.html', 
                         job=job, 
                         has_applied=has_applied,
                         user_application=user_application)

@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
@login_required
def apply_job(job_id):
    if current_user.is_admin:
        flash('Admins cannot apply for jobs.', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))
    
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    existing_application = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first()
    if existing_application:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('job_detail', job_id=job_id))
    
    form = ApplicationForm()
    if form.validate_on_submit():
        # Handle file upload
        resume_file = form.resume.data
        filename = secure_filename(f"{current_user.id}_{job_id}_{resume_file.filename}")
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        resume_file.save(resume_path)
        
        application = Application(
            job_id=job_id,
            user_id=current_user.id,
            cover_letter=form.cover_letter.data,
            resume_filename=filename
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('job_detail', job_id=job_id))
    
    return render_template('job_detail.html', job=job, form=form, applying=True)

@app.route('/my-applications')
@login_required
def my_applications():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    applications = Application.query.filter_by(user_id=current_user.id)\
                                  .order_by(Application.applied_at.desc())\
                                  .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('my_applications.html', applications=applications)

@app.route('/download-resume/<int:application_id>')
@login_required
def download_resume(application_id):
    application = Application.query.get_or_404(application_id)
    
    # Check if user has permission to download this resume
    if not (current_user.is_admin or current_user.id == application.user_id):
        abort(403)
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], application.resume_filename)

# Admin Routes
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Get statistics for admin dashboard
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    pending_applications = Application.query.filter_by(status='pending').count()
    total_users = User.query.filter_by(is_admin=False).count()
    
    # Recent activity
    recent_jobs = Job.query.order_by(Job.posted_at.desc()).limit(5).all()
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_jobs=total_jobs,
                         active_jobs=active_jobs,
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         total_users=total_users,
                         recent_jobs=recent_jobs,
                         recent_applications=recent_applications)

@app.route('/admin/jobs')
@login_required
@admin_required
def admin_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    jobs = Job.query.order_by(Job.posted_at.desc())\
                   .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin_jobs.html', jobs=jobs)

@app.route('/admin/post-job', methods=['GET', 'POST'])
@login_required
@admin_required
def post_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            job_type=form.job_type.data,
            salary_range=form.salary_range.data,
            description=form.description.data,
            requirements=form.requirements.data,
            posted_by=current_user.id,
            application_deadline=form.application_deadline.data
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('admin_jobs'))
    
    return render_template('post_job.html', form=form)

@app.route('/admin/edit-job/<int:job_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('admin_jobs'))
    
    return render_template('post_job.html', form=form, job=job, editing=True)

@app.route('/admin/toggle-job/<int:job_id>')
@login_required
@admin_required
def toggle_job_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    
    status = "activated" if job.is_active else "deactivated"
    flash(f'Job {status} successfully!', 'success')
    return redirect(url_for('admin_jobs'))

@app.route('/admin/applications')
@login_required
@admin_required
def admin_applicants():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    job_id = request.args.get('job_id', type=int)
    status_filter = request.args.get('status', '')
    
    query = Application.query
    
    if job_id:
        query = query.filter_by(job_id=job_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    applications = query.order_by(Application.applied_at.desc())\
                       .paginate(page=page, per_page=per_page, error_out=False)
    
    # Get all jobs for filter dropdown
    jobs = Job.query.order_by(Job.title).all()
    
    return render_template('admin_applicants.html', 
                         applications=applications,
                         jobs=jobs,
                         current_job_id=job_id,
                         current_status=status_filter)

@app.route('/admin/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def review_application(application_id):
    application = Application.query.get_or_404(application_id)
    form = ApplicationStatusForm(obj=application)
    
    if form.validate_on_submit():
        old_status = application.status
        application.status = form.status.data
        application.notes = form.notes.data
        application.reviewed_at = datetime.utcnow()
        db.session.commit()

        # Send email if status changed to accepted
        if old_status != 'accepted' and application.status == 'accepted':
            user = User.query.get(application.user_id)
            if user and user.email:
                try:
                    msg = Message(
                        subject='Your Job Application Has Been Approved',
                        recipients=[user.email],
                        body=f"""
Hello {user.full_name},

Congratulations! Your application for the job '{application.job.title}' at {application.job.company} has been approved.

You may receive further instructions from the employer soon.

Best regards,
Job Portal Team
                        """
                    )
                    mail.send(msg)
                except Exception as e:
                    app.logger.error(f"Failed to send approval email: {e}")

        flash('Application status updated successfully!', 'success')
        return redirect(url_for('admin_applicants'))
    
    return render_template('admin_applicants.html', 
                         application=application, 
                         form=form, 
                         reviewing=True,
                         applications=None)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
