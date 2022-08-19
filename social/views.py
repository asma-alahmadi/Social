import json
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def login_view(request):
    storage = messages.get_messages(request)
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None :
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "social/login.html", {
                "message": "Invalid username and/or password.",
                "messages": storage
            })
    else:
        return render(request,"social/login.html")


''' Logout View '''
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


''' Register View '''
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']

        #Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        
        if password != confirmation:
            return render(request, "social/register.html", {
                "message": "Passwords must match"
            })

        # Attemp to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "social/register.html", {
                "message": "Username already taken"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "social/register.html") 



''' LIKE VIEWS '''
@login_required
@csrf_exempt
def like(request):
    user = request.user
    if request.method !='PUT':
        return JsonResponse({'erroe': "PUT request required"}, status=400)
    data = json.loads(request.body)
    post_id = data.get("post_id", "")
    count = data.get("count", "")
    post = Post.objects.get(pk=post_id)
    is_liked = False
    if post in user.likes.all():
        is_liked = True
        post.likes.remove(user)
        post.likes.count = count
        is_liked = False
    else:
        is_liked = False
        post.likes.add(user)
        post.likes.count = count
        is_liked = True
    post.likes.count = count
    post.save()
    return JsonResponse({"message": "Post liked successfully", "is_liked": is_liked, "likes_num": str(post.likes.count)}, status=201)

''' share View '''
def share(request):
    storage = messages.get_messages(request)
    pst = Post()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must log in first, so you can add posts.")
            return redirect('login')
        pst.post = request.POST.get('post')
        pst.user = request.user
        pst.save()
        if request.FILES.getlist('imgs'):
            files = request.FILES.getlist('imgs')
            if len(files) > 4:
                raise Exception("Only four images allowed")
            else:
                for f in files:
                    images=PostImage.objects.create(post=pst, imgs=f)
                    images.save()
            return redirect('index')

        return redirect('index')
    post = Post.objects.all().order_by('-date')
    return render(request, 'social/index.html', {"posts":post, "messages": storage,  })


''' Render only one post by its id '''
def singlePost(request, id):
    post = Post.objects.get(id= id)
    post_comments = Comment.objects.all().filter(post_id=id).annotate(like_count=Count('comment_like')).order_by('-like_count')
    return render(request, "social/singlePost.html", {"post": post, "post_comments": post_comments})


''' View for add comment to post '''
@csrf_exempt
def comment(request, id):
    storage = messages.get_messages(request)
    if not request.user.is_authenticated:  
        messages.error(request, "You must log in first, so you can add comments.")
        return redirect('login')
    post = Post.objects.get(id=id)
    user = request.user
    comment = Comment()
    if request.method == "POST":
        comment.comment = request.POST.get('comment')
        comnt = Comment.objects.create(user=user, post=post, comment=comment.comment)
        comnt.save()    
        return redirect('post', id=id)  
                  
    else: 
        return render(request, "social/singlePost.html", {"messages": storage, })


''' View to like comment '''
@login_required
@csrf_exempt
def like_comment(request):
    user = request.user
    if request.method != 'PUT':
        return JsonResponse({'error': "PUT request required"}, status=400)
    data = json.loads(request.body)
    comment_id = data.get("comment_id", "")
    count = data.get("count", "")
    comment = Comment.objects.get(pk=comment_id)
    is_liked = False
    if comment in user.com_like.all():
        is_liked = True
        comment.comment_like.remove(user)
        comment.comment_like.count = count
        is_liked = False
    else:
        is_liked = False
        comment.comment_like.add(user)
        comment.comment_like.count = count
        is_liked = True
    comment.comment_like.count = count
    comment.save()
    return JsonResponse({"message": "Comment liked successfully", "is_liked": is_liked, "likes_num": str(comment.comment_like.count)}, status=201)



''' view to delete post '''
def delete_post(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    if user == post.user:
        post.delete()
        messages.info(request, "Post successfully deleted.")
    else:
        messages.error(request, "You can not delete this 'Post'.")
    return redirect('index')


''' view to delete comment '''
def delete_comment(request, id):
    user = request.user
    comment = get_object_or_404(Comment, id=id)
    if user == comment.user:
        comment.delete()
        messages.info(request, "Comment successfully deleted.")
    else:
        messages.error(request, "You can not delete this 'Comment'.")
    return redirect('post', comment.post.id)


''' View to edit post '''
@csrf_exempt
def edit(request):
    if request.method != 'PUT':
        return JsonResponse({"erroe": "PUT request required"}, status=400)
    data = json.loads(request.body)
    data_id = data.get("post_id", "")
    post = Post.objects.get(id = data_id)
    content = data.get("content", "")
    if content:
        if request.user != post.user:
            return JsonResponse({"error": "Only the auther can edit this post"})
        post.post = content
    post.save()
    return JsonResponse({"message": "Post edited successfully"}, status=201)


'''  View to edit comment '''
@csrf_exempt 
def edit_comment(request):
    if request.method != 'PUT':
       return JsonResponse({'error': "PUT request required."}, status=400)
    data = json.loads(request.body)
    data_id = data.get("comment__id", "")
    comment = Comment.objects.get(id = data_id)
    content = data.get("comment_content", "")
    if content:
        if request.user != comment.user:
            return JsonResponse({"error": "Only the auther can edit this comment."})
        comment.comment = content
    comment.save()
    return JsonResponse({"message": "The comment edited successfully."}, status=201)