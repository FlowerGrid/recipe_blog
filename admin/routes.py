from flask import Blueprint, render_template, request, session, redirect, url_for, render_template, abort, jsonify, flash
from admin.forms import LoginForm, RecipeForm, UserInfoForm, UpdatePasswordForm, BlogForm
from functools import wraps
import utils.db_helpers as db_helpers
from utils.models import Recipe, BlogPost

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static', static_url_path='/static')

# CATEGORIES = db_helpers.get_all_categories()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper


@admin_bp.route('/')
@login_required
def admin_dash():
    data = {
        'page_name': 'Dashboard'
    }
    return render_template('admin/dashboard.html', data=data)


@admin_bp.route('/wizard-lash', methods=['GET', 'POST'])
def login():
    data = {
        'page_name': 'Login'
    }
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        password = form.password.data
        
        user_check = db_helpers.query_user(username, password)

        if user_check:
            session['username'] = username
            flash(f'welcome, {session['username']} successfully logged in!', 'success')
            return redirect(url_for('admin.admin_dash'))
        else:
            flash(f'Incorrect username or password.', 'danger')
    return render_template('admin/login.html', data=data, form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    data = {
        'page_name': 'login'
    }
    session.clear()
    flash('Logged out')
    return redirect(url_for("admin.login"))


@admin_bp.route('/settings')
@login_required
def admin_settings():
    user = db_helpers.get_user_info(session['user_id'])
    data = {
        'page_name': 'Settings'
    }
    return render_template('admin/settings.html', data=data, user=user)


@admin_bp.route('/upadate-info', methods=['GET', 'POST'])
@login_required
def update_user_info():
    user = db_helpers.get_user_info(session['user_id'])
    info_form = UserInfoForm(obj=user)

    data = {
        'page_name': 'Update Info'
    }

    if info_form.validate_on_submit():
        db_helpers.update_user(info_form)
        return redirect(url_for('admin.admin_settings'))
    
    return render_template(
        'admin/update-user-info.html',
        user=user, data=data,
        info_form=info_form,
        )


@admin_bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def change_pw():
    form = UpdatePasswordForm()
    data = {'page_name': 'Reset Password'}
    if form.validate_on_submit():
        print()
        print('password click')
        print()        
        check, message = db_helpers.change_pw(form)
        if check:
            flash(message)
            return redirect(url_for('admin.admin_settings'))
        else:
            flash(message)
            return redirect(url_for('admin.change_pw'))


    return render_template('admin/change-pw.html', data=data, form=form)


@admin_bp.route('/my-recipes')
@login_required
def admin_all_recipes():
    all_recipes = db_helpers.get_all_recipes()
    data = {
        'page_name': 'My Recipes',
        'type': 'Recipe'
    }
    return render_template('admin/view-objects-list.html', data=data, all_objects=all_recipes)


@admin_bp.route('/blog-posts')
def admin_all_blogs():
    blogs = db_helpers.get_active_blog_posts()
    data = {
        'page_name': 'Blog Posts',
        'type': 'Blog'
    }
    return render_template('admin/view-objects-list.html', data=data, all_objects=blogs)


@admin_bp.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    # form.category.choices = [(cat.id, cat.name) for cat in CATEGORIES]
    data = {
        'page_name': 'Add Recipe',
    }
    if form.validate_on_submit():
        rel_attr_name = 'tags_in_recipe'
        db_helpers.gather_form_data_unified(Recipe, form, rel_attr_name)

        return redirect(url_for('admin.admin_all_recipes'))

    return render_template('admin/add-recipe.html', form=form, data=data) # Removed - categories=CATEGORIES


@admin_bp.route('/new-blog-post', methods=['GET', 'POST'])
def new_blog_post():
    form = BlogForm()
    # form.category.choices = [(cat.id, cat.name) for cat in CATEGORIES]
    data = {
        'page_name': 'New Post'
    }
    if form.validate_on_submit():
        print('form')
        print(request.form)
        print('form end')
        rel_attr_name = 'tags_in_blog_post'
        db_helpers.gather_form_data_unified(BlogPost, form, rel_attr_name)

        return redirect(url_for('admin.admin_all_blogs'))

    return render_template('admin/blog-post.html', form=form, data=data) # Removed - categories=CATEGORIES


@admin_bp.route('/edit-recipe/<int:recipe_id>')
@login_required
def edit_recipe(recipe_id):
    recipe = db_helpers.get_joined_recipe_from_db('id', recipe_id)
    form = RecipeForm(obj=recipe)
    tags_list = [t.name for t in recipe.tags_in_recipe]
    # form.category.choices = [(cat.id, cat.name) for cat in CATEGORIES]
    data = {
        'page_name': 'Edit Recipe',
        'img': recipe.image_url,
        'tags_list': tags_list
    }
    return (render_template('admin/add-recipe.html', data=data, form=form))


@admin_bp.route('/edit-blog/<int:blog_id>')
@login_required
def edit_blog_post(blog_id):
    post = db_helpers.get_single_blog_post_by_id(blog_id)
    form = BlogForm(obj=post)
    tags_list = [t.name for t in post.tags_in_blog_post]
    # form.category.choices = [(cat.id, cat.name) for cat in CATEGORIES]
    data = {
        'page_name': 'Edit Blog',
        'img': post.image_url,
        'tags_list': tags_list
    }
    return (render_template('admin/blog-post.html', data=data, form=form))


@admin_bp.route('/toggle-active-status', methods=['POST'])
@login_required
def toggle_active_status():
    data = request.get_json()
    target_id = data.get('target_id')
    page_name = data.get('page_name').lower()

    # Add conditional here to select recipe or product link
    if 'recipe' in page_name:
        target_obj = db_helpers.get_single_recipe_by_id(target_id)
    elif 'blog' in page_name:
        target_obj = db_helpers.get_single_blog_post_by_id(target_id)

    if target_obj:
        db_helpers.toggle_active_status_in_db(target_obj)
        return jsonify({'success': True, 'new_status': target_obj.is_active})
    return jsonify({'success': False}), 404


