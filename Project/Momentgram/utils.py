from .models import Post, Profile, Follow, Message, Comment, Like
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
    Message.objects.create(sender=sender, reciever = reciever, text = message)
    return True

def getChat(user1, user2):
    return Message.objects.filter(Q(sender=user1, receiver=user2)|Q(sender=user2, receiver=user1))

def getUsersSorted(user, pattern):
    toReturn = []
    users = User.objects.filter(username__icontains=pattern)
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

#Given a user and post returns True if that user can give a like to that certain Post
def isLikeable(user,post):
    return not(Like.objects.filter(user=user,post=post).exists())

#Given a certain post returns the number of likes
def getNumberOfLikes(post):
    if Like.object.filter(post=post).exists():
        return len(Like.object.filter(post=post))
    else:
        return 0

#Creates a comment linked to a user and a post
def createComment(user,post,comment):
    Comment.objects.create(user=user,post=post,comment=comment)
    return True