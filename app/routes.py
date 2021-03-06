from app import api
from resource.contact import ContactListResource, ContactResource
from resource.post import PostListResource, PostResource
from resource.user import MeResource, UserListResource, UserResource
from resource.signup import SignupResource
from resource.login import LoginResource
from resource.topic import TopicListResource, TopicResource
from resource.comment import CommentListResource, CommentResource

# Signup a acount
api.add_resource(SignupResource, "/v1/api/signup")
# Login to system
api.add_resource(LoginResource, "/v1/api/login")
# user api
api.add_resource(UserListResource, "/v1/api/users")
api.add_resource(UserResource, "/v1/api/user/<int:user_id>", "/v1/api/user")
api.add_resource(MeResource, "/v1/api/me")

# contact api
api.add_resource(ContactListResource, "/v1/api/contacts")
api.add_resource(ContactResource, "/v1/api/contact/<int:contact_id>", "/v1/api/contact")

# topic api
api.add_resource(TopicListResource, "/v1/api/topics")
api.add_resource(TopicResource, "/v1/api/topic/<int:topic_id>", "/v1/api/topic")

# post api
api.add_resource(PostListResource, "/v1/api/posts")
api.add_resource(PostResource, "/v1/api/post/<int:post_id>", "/v1/api/post")

# comment api
api.add_resource(CommentListResource, "/v1/api/comments")
api.add_resource(CommentResource, "/v1/api/comment/<int:comment_id>", "/v1/api/comment")