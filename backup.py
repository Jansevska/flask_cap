# @app.route('/user/<username>/edit', methods=["GET", "POST"])
# @login_required
# def edit_user(user_id):
#     user = db.session.get(User, user_id)
#     if not user:
#         flash('User not found')
#         return redirect(url_for('login'))
#     if current_user != user_id:
#         flash('You can only edit your own profile!')
#         return redirect(url_for('login', current_user=current_user, user_id=user_id))
    
#     # Create an instance of the SignUpForm
#     form = SignUpForm()
    
#         # If form submitted, update the user profile
#     if form.validate_on_submit():
#         # update the post with the for data
#         user.first_name = form.first_name.data
#         user.last_name = form.last_name.data
#         user.username = form.username.data
#         user.email = form.email.data
#         user.password = form.password.data
#         # Commit to the database
#         db.session.commit()
#         flash(f'{user.username} has been edited.', 'success')
#         return redirect(url_for('user'))

#     # Pre-populate the form with the post's data
#     form.first_name.data = user.first_name
#     form.last_name.data = user.last_name
#     form.username.data = user.username
#     form.email.data = user.email
#     form.password.data = user.password
    
#     return render_template('edit_post.html', user=user, form=form)