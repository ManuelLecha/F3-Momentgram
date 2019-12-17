from .models import Post, Profile, Follow, Message, Comment, Like
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files import File
import os
from urllib import request
from django.core.files.temp import NamedTemporaryFile


def createPost(description, owner, image):
    #Need to check if it works creating a post without description
    newPost = Post.objects.create(user=owner, image=image, description = description)
    return newPost


def deletePost(post):
    post.delete()

def getUserPosts(user):
    return Post.objects.filter(user=user)


def follow(user, user2follow):
    Follow.objects.create(follower=user, following=user2follow)


def unfollow(user, user2unfollow):
    Follow.objects.filter(follower=user, following=user2unfollow)[0].delete()


def getFollowers(user):
    followers = Follow.objects.filter(following=user)
    return [x.follower for x in followers]


def getFollowing(user):
    following = Follow.objects.filter(follower=user)
    return [x.following for x in following]

def createUser(username, password, mail, first= None, last=None):
    if not isUserExisting(username,mail):
        user = User.objects.create_user(username,mail,password)
        if first:
            user.first_name = first
        if last:
            user.last_name = last
        user.save()
        profile = getProfile(user)
        image_url = "https://st2.depositphotos.com/1003591/7970/i/950/depositphotos_79702338-stock-photo-potato-with-funny-face.jpg"
        img_temp = NamedTemporaryFile()
        img_temp.write(request.urlopen(image_url).read())
        img_temp.flush()

        profile.image.save("inici.jpg", File(img_temp))
        profile.save()
        return user
    else:
        return None


def isUserExisting(username, mail):
    return User.objects.filter(username=username).exists() or User.objects.filter(email=mail).exists()

def getUser(username):
    if User.objects.filter(username=username):
        return User.objects.filter(username=username)[0]
    else:
        return None

def getProfile(user):
    if Profile.objects.filter(user=user):
        return Profile.objects.filter(user=user)[0]
    else:
        return None


def getPost(id):
    if Post.objects.filter(id=id):
        return Post.objects.filter(id=id)[0]
    else:
        return None

def getTimeline(username):
    posts = []
    if getFollowing(username):
        for user in getFollowing(username):
            for post in getUserPosts(user):
                posts.append(post)
        return sorted(posts, key=lambda x: x.date, reverse=True)
    else:
        return posts


def sendMessage(sender,reciever,message):
    Message.objects.create(sender=sender, receiver = reciever, text = message)
    return True

def getChat(user1, user2):
    return Message.objects.filter(Q(sender=user1, receiver=user2)|Q(sender=user2, receiver=user1))

def getUsersSorted(user, pattern):
    toReturn = []
    users = User.objects.filter(Q(username__icontains=pattern)|Q(first_name__icontains=pattern))
    followers = getFollowers(user)
    following = getFollowing(user)

    for u in users:
        if u in followers and u in following:
            toReturn.append(u)
            users = users.exclude(username=u)

    for u in users:
        if u in following:
            toReturn.append(u)
            users = users.exclude(username=u)

    for u in users:
        if u in followers:
            toReturn.append(u)
            users = users.exclude(username=u)

    for u in users:
        toReturn.append(u)

    return toReturn

#Given a user, it gets all the messages sent and received by him, orders them and
#returns the last message that we have with the other user
def getChatPreviews(user):
    if Message.objects.filter(Q(sender=user) | Q(receiver=user)):
        sorted_messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('date')
        users = set()
        message_previews = []
        for message in sorted_messages:
            other_user = message.sender if user == message.receiver else message.receiver
            if other_user not in users:
                message_previews.append((other_user,message))
                users.add(user)
        return message_previews
    else:
        return None

#Given a post returns the list of comments associated with it ordered by date
def getPostComments(post):
    return Comment.objects.filter(post=post)

#Creates an univocal link between user and a post called like
def createLike(user,post):
    Like.objects.create(user=user, post=post)


#Unlikes a like for a post that a certain user has given like to
def unlike(user,post):
    if Like.objects.filter(user=user,post=post).exists():
        Like.objects.filter(user=user, post=post).delete()
        return True
    else:
        return False
      
#Given a user and post returns True if that user can give a like to that certain Post
def isLikeable(user,post):
    return not(Like.objects.filter(user=user,post=post).exists())

#Given a certain post returns the number of likes
def getNumberOfLikes(post):
    if Like.objects.filter(post=post).exists():
        return len(Like.objects.filter(post=post))
    else:
        return 0
#Creates a comment linked to a user and a post
def createComment(user,post,comment):
    Comment.objects.create(user=user,post=post,comment=comment)
    return True

def updateUser(user, firstname=None, lastname=None, password=None, bio=None, image=None):
    profile = getProfile(user)
    if firstname:
        user.first_name = firstname
    if lastname:
        user.last_name = lastname
    if password:
        user.set_password(password)
    if bio:
        profile.bio = bio
    if image:
        profile.image = image
    user.save()
    profile.save()