import os, datetime
from App.Repository import *
from helpers import generate_unique_code, hash_password
# from Orgs.models import OrganisationUser, OrgTypeOrg, OrgTypeOrgUser
from models import User, UserDetail, UserToken


##
# AuthRepository - For all database transactions
##
class AuthRepository():

    ##
    # To Store the data
    ##
    def store(self, model, data):
        result = store(model, data)
        return result

    def update(self, model, filterBy, data):
        result = update(model, filterBy, data)
        return result

    def fetch_all(self, model):
        result = fetchAll(model)
        return result

    def filter_attribute(self, model, findBy):
        result = filter_attribute(model, findBy).first()
        return result

    def delete(self, model, findBy):
        result = delete(model, findBy)
        return result


    def add_user_class(self, model, org_user, cls_id):
        data = {'id': generate_unique_code(), 'org_user_id': org_user.id, 'user_type_id': cls_id}
        return store(model, data)


    def delete_all_user_class(self, org_user):
        return delete(OrgTypeOrgUser, { 'org_user_id': org_user.id })


    def get_roles_in_org(self, org, user):
        org_user = filter_attribute(OrganisationUser, {'user_id': user[0].id, 'organisation_id': org.id})
        org_type_id = OrgTypeOrg.objects.values_list('id', flat=True).filter(org_id=org.id)
        # org_type = filter_attribute(OrgTypeOrg, {'org_id': org.id})
        # return OrgTypeOrgUser.objects.filter(org_user_id=org_user[0].id, user_type_id__in=org_type_id)
        return filter_attribute(OrgTypeOrgUser, {'org_user_id': org_user[0].id, 'user_type_id__in': org_type_id})


    def get_roles_in_org_user(self, org_user, class_id):
        # print class_id
        result = filter_attribute(OrgTypeOrgUser, {'id': class_id})
        return result[0]

class UserTokenRepository():
    '''
    ' To Store the data
    '''
    def store(self, model, data):
        result = store(model, data)
        return result

    '''
    check valid token
    '''
    def check_valid_token(self, model, token):
        findBy = {
            'token' : token,
        }
        result = filter_attribute(model, findBy).filter(model.expires_at > datetime.datetime.now()).first()
        return result

    '''
    delete token
    '''
    def deleteToken(self, model, token):
        return delete(model, {'token' : token})


class UserRepository():
    
    def create_user(self, request):
        details = self.create_user_details(request)
        data = {'id': request.get('user_id'), 'email': request.get('email'), 'display_name': request.get('display_name'),
                'user_detail_id': details.id, 'password': hash_password('sync#124'), 'is_password_change_required': True,
                'confirmation_code': get_confirmation_code(request.get('email'))}
        return Users.objects.create(**data)


    def create_user_details(self, request):
        data = {'first_name':request.get('display_name')}
        return UserDetails.objects.create(**data)


    def find_or_create_user(self, request):
        user = Users.objects.filter(email=request.get('email')).first()
        if user:
            return user, 'invitation_email'

        user_details = UserDetails.objects.create(first_name=request.get('display_name'))
        data = {'id': generate_unique_code(), 'email': request.get('email'), 'display_name': request.get('display_name'),
            'user_detail_id': user_details.id, 'password': hash_password('sync#125'), 'is_password_change_required': True,
            'confirmation_code': get_confirmation_code(request.get('email')) }
        return Users.objects.create(**data), 'activation_email'

    def get_user_by_email(self, email):
        return Users.objects.filter(email=email).first()

