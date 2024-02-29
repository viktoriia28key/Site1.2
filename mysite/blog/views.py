from django.shortcuts import render ,get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .models import Post, PostPoint
from django.views.generic import ListView
from .models import Comment
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count

class PostListViev(ListView):
    queryset=Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:

        posts = paginator.page(1)
    except EmptyPage:

        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})





def post_detail(request, year, month, day, post):
    post_object = get_object_or_404(Post, slug=post, status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    post_points = PostPoint.objects.filter(post=post_object)

    comments = post_object.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            new_comment = Comment(post=post_object, name=cd['name'], email=cd['email'], body=cd['body'])
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids=post_object.tags.values_list('id',flat=True)
    similar_posts=Post.objects.filter(tags__in=post_tags_ids,
                                      status='published').exclude(id=post_object.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post_object,
                                                     'post_points': post_points,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts
                                                     })