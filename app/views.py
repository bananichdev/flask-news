from flask import render_template, redirect, url_for

from . import app, db
from .forms import NewsForm
from .models import Category, News


@app.route('/')
def index():
    news_list = News.query.all()[::-1]
    categories_list = Category.query.all()
    return render_template(
        'index.html',
        news=news_list,
        categories_list=categories_list
    )


@app.route('/news_detail/<int:id>')
def news_detail(id):
    categories_list = Category.query.all()
    news = News.query.get(id)
    return render_template(
        'news_detail.html',
        news=news,
        categories_list=categories_list
    )


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    categories_list = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data[0]
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news_detail', id=news.id))
    return render_template(
        'add_news.html',
        form=form,
        categories_list=categories_list
    )


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news[::-1]
    categories = Category.query.all()
    return render_template(
        'category.html',
        news=news,
        category=category,
        categories_list=categories
    )
