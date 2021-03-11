import os
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Product
from . import db, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from PIL import Image
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user, posts=Product.query.all(), home=True, path='../images/bana-kanjiza-sta-posetiti-630x630.png')

@views.route('/new-post', methods=['GET', 'POST'])
@login_required
def newPost():
    if request.method == 'POST':
        productName = request.form.get('productName')
        desc = request.form.get('desc')
        cost = request.form.get('cost')
        image = request.files['image']
        user = current_user
        posts = Product.query.filter_by(userId=user.id).all()


        if len(posts) < 2 or user.admin: 
            if len(productName) > 50 or len(productName) < 3:
                flash('Product name needs to be maximum 50 and minimum 3 charecters', category='error')
            elif len(desc) > 250 or len(desc) < 10:
                flash('Description name needs to be maximum 250 charecters and minimum 10 charecters', category='error')
            elif len(str(cost)) < 1:
                flash('You have to have a cost.', category='error')
            elif not image:
                flash('You have to select product image', category='error')
            elif not image.mimetype in ALLOWED_EXTENSIONS:
                flash('That extension is not allowed', category='error')
            elif len(str(image).split())-2 > 1:
                print(len(str(image).split()))
                flash('Image must be 1 word long', category='error')
            elif not isASCII(str(image)):
                flash('Image must be in alphabet', category='error')
            else:
                imgFolder = os.path.join('website', 'static', 'images')
                newProduct = Product(productName=productName, desc=desc, cost=abs(int(cost)), userId=current_user.id, userName=current_user.firstName, imagePath=os.path.join(imgFolder, secure_filename(image.filename)), imageName=secure_filename(image.filename))
                print(os.getcwd())
                image.save(os.path.join('website','static','images', image.filename))
                db.session.add(newProduct)
                db.session.commit()
                flash('Product added', category='success')
                return redirect(url_for('views.home'))
        else:
            flash('You have reach post limit', category='error')

    return render_template('newPost.html', user=current_user)

@views.route('/delete-post', methods=['POST'])
def deletePost():
    post = json.loads(request.data)
    postId = post['postId']
    post = Product.query.get(postId)
    if post:
        if post.userId == current_user.id or current_user.admin:
            os.chdir(os.path.join(os.getcwd(),'website', 'static', 'images'))
            os.remove(post.imageName)
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted.', category='success')
        else:
            flash('You are not authorized to do that.', category='error')
    return ''
    
@views.route('/report-post', methods=['POST'])
def reportPost():
    postId = json.loads(request.data)
    post = Product.query.filter_by(productId=postId).first()
    user = User.query.filter_by(id=post.userId).first()
    reported = [user.firstName, post.productName]
    reports = []

    file = open('website/reported.txt', 'r')
    for line in file.readlines():
        text = line.split()
        reports.append(text)
    file.close()
    file = open('website/reported.txt', 'a')
    if reported not in reports:
        file.write(user.firstName + ' ' + post.productName + '\n')
    
    return redirect(url_for('views.home'))

@views.route('/images/<id>')
def diplayImages(id):
    product = Product.query.filter_by(productId=id[1:-1]).first()
    return render_template('displayImage.html', imageName=os.path.join('images/', product.imageName), user=current_user)

def isASCII(string):
    return len(string) == len(string.encode())
