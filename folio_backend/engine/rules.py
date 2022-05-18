import rules
from rest_framework.permissions import BasePermission
from rules import always_allow, always_deny, is_staff


@rules.predicate
def is_portfolio_owner(db_user, db_portfolio):
    if db_portfolio.owner == db_user:
        return True
    return False


@rules.predicate
def is_follow_owner(db_user, db_follow):
    if db_follow.user == db_user:
        return True
    return False


@rules.predicate
def is_follower(db_user, db_portfolio):
    db_follows = list(db_portfolio.follow_set.all())
    return any([is_follow_owner(db_user, db_follow) for db_follow in db_follows])


@rules.predicate
def is_transaction_owner(db_user, db_transaction):
    return is_portfolio_owner(db_user, db_transaction.portfolio)


@rules.predicate
def is_portfolio_public(db_user, db_portfolio):
    if db_portfolio.is_public:
        return True
    return False


# Permisssions Rules
rules.add_perm("engine.user.create", always_deny)  # Use IAM to create a new user
rules.add_perm("engine.user.retrieve", always_allow)
rules.add_perm("engine.user.update", always_allow)
rules.add_perm("engine.user.delete", is_staff)

rules.add_perm("engine.portfolio.create", always_allow)
rules.add_perm("engine.portfolio.retrieve", is_portfolio_owner | is_follower | is_staff | is_portfolio_public)
rules.add_perm("engine.portfolio.update", is_portfolio_owner | is_staff)
rules.add_perm("engine.portfolio.delete", is_portfolio_owner | is_staff)

rules.add_perm("engine.follow.create", always_allow)
rules.add_perm("engine.follow.retrieve", is_follow_owner | is_staff)
rules.add_perm("engine.follow.update", is_follow_owner | is_staff)
rules.add_perm("engine.follow.delete", is_staff)

rules.add_perm("engine.transaction.create", is_portfolio_owner | is_staff)
rules.add_perm("engine.transaction.retrieve", is_portfolio_owner | is_follower | is_staff)
rules.add_perm("engine.transaction.update", is_staff)
rules.add_perm("engine.transaction.delete", is_staff)

rules.add_perm("engine.stock.create", is_staff)
rules.add_perm("engine.stock.retrieve", always_allow)
rules.add_perm("engine.stock.update", is_staff)
rules.add_perm("engine.stock.delete", is_staff)

# User API
class UserCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.user.create")


class UserRetrievePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.user.retrieve")


class UserUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.user.update")


class UserDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.user.delete")


# Portfolio API
class PortfolioCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.portfolio.create")


class PortfolioRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.portfolio.retrieve", obj)


class PortfolioUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.portfolio.update", obj)


class PortfolioDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.portfolio.delete", obj)


# Follow API
class FollowCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("engine.follow.create")


class FollowRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.follow.retrieve", obj)


class FollowUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.follow.update", obj)


class FollowDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.follow.delete", obj)


# Transaction API
class TransactionCreatePermission(BasePermission):
    def has_object_permission(self, request, view, db_portfolio):
        # for this permission, please use a Portfolio object as a argument
        return request.user.has_perm("engine.transaction.create", db_portfolio)


class TransactionRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, db_portfolio):
        return request.user.has_perm("engine.transaction.retrieve", db_portfolio)


class TransactionUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.transaction.update", obj)


class TransactionDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.transaction.delete", obj)


# Stock API
class StockCreatePermission(BasePermission):
    def has_permission(self, request, view, obj):
        return request.user.has_perm("engine.stock.create")


class StockRetrievePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.stock.retrieve", obj)


class StockUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.stock.update", obj)


class StockDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm("engine.stock.delete", obj)
