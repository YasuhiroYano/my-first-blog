from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('app:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

from django.http import HttpResponse
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# グラフ作成

def setPlt():   
    # 折れ線グラフを出力
    # TODO: 本当はpkを基にしてモデルからデータを取得する。
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12])
    y = np.array([20, 90, 50, 30, 100, 80, 10, 60, 40, 70,35,20])
    plt.plot(x, y)
# svgへの変換
def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

def graph(request):   
      return render(request, 'blog/graph.html')

def get_svg(request):
    setPlt()       # create the plot
    svg = pltToSvg() # convert plot to SVG
    plt.cla()        # clean up plt so it can be re-used
    return HttpResponse(svg, content_type='image/svg+xml')

def get_png(request):
    wine=pd.read_csv('http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv',sep=';')
    x=wine.alcohol
    y=wine.pH
    plt.scatter(x,y)
    plt.xlabel('alchol')
    plt.ylabel('pH')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    png = buf.getvalue()
    buf.close()
    plt.cla()        # clean up plt so it can be re-used
    return HttpResponse(png, content_type='image/png+xml')