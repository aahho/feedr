from models import *
import datetime
import env
from sqlalchemy.orm import  sessionmaker,session
from sqlalchemy import create_engine

session = session.Session(bind=create_engine(env.SQLALCHEMY_DATABASE_URI))

def filterByAttribute(modelName, filterKeys):
    return modelName.query.get(filterKeys)

def filterByAttributePaginated(modelName, filterKeys, item=25, page=1, sortBy={'created_at':'desc'}):
	orderBy = []
	for column, order in sortBy.iteritems() :
		orderBy.append(getattr(getattr(modelName, column), order)())
	return modelName.query.filter_by(**filterKeys).order_by(*orderBy).paginate(page=int(page), per_page=int(item), error_out=False)

def authenticate(modelName, access_token):
    return modelName.query.filter(access_token=access_token, expires_at__gte=datetime.datetime.now())

def authenticate_admin(modelName, user_id):
    return modelName.query.filter(id=user_id)

def filter_attribute(modelName, filterKeys):
    return modelName.query.filter_by(**filterKeys)

def update(modelName, filterKeys, updateWith):
    updateWith.update({'updated_at':datetime.datetime.now()})
    return modelName.query.filter(**filterKeys).update(**updateWith) 

def fetchAll(modelName):
    return modelName.query.all()

def fetchSelect(modelName, select_params):
	from sqlalchemy.orm import load_only
	# return modelName.query.options(load_only(select_params)).all()
	return modelName.query.options(load_only(*select_params)).all()

def store(modelName, values):
	modelInstance = modelName(**values)
	session.add(modelInstance)
	session.commit()
	return modelInstance

def delete(modelName, filterKeys):
	rows = session.query(modelName).filter(modelName.token==filterKeys['token']).delete()
	# print dd.delete(synchronize_session = False)
	session.commit()
	return rows








