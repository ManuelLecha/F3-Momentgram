from .models import Post, Profile, Follow, Message
from django.contrib.auth.models import User
from django.db.models import Q


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

def getPost(id):
    if Post.objects.filter(id=id):
        return Post.objects.filter(id=id)[0]
    else:
        return None

def sendMessage(sender,reciever,message):
    Message.objects.create(sender=sender, reciever = reciever, text = message)
    return True

def getChat(user1, user2):
    return Message.objects.filter(Q(sender=user1, receiver=user2)|Q(sender=user2, receiver=user1))

def getUsersSortedToChat(user, pattern):
    toReturn = []
    users = User.object.filter(username__icontains=pattern)
    followers = getFollowers(user)
    following = getFollowing(user)

    for u in users:
        if u in followers and u in following:
            toReturn.append(u)
            users.delete(u)

    for u in users:
        if u in following:
            toReturn.append(u)
            users.delete(u)

    for u in users:
        if u in followers:
            toReturn.append(u)
            users.delete(u)

    for u in users:
        toReturn.append(u)

    return toReturn

