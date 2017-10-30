from flask import Flask, request, url_for
import datetime
FB_WT = 0.2
LD_WT = 0.4
PR_WT = 0.3
RDD_WT = 0.6
GO_WT = 0.7
devience = 0.85
'''
algo for duck rank calculatio
'''
def duck_rank_algo(article, alexa_rank, shares, published_at=datetime.datetime.now()):
    # general devience for all the articles

    days_published_before = (datetime.datetime.now() - published_at).days \
        if (datetime.datetime.now() - published_at).days > 0 else 1
    reddit_count = (shares['reddit']['ups'] if 'reddit' in shares else 0) / days_published_before
    facebook_count = (shares['facebook']['share_count'] if 'facebook' in shares else 0) / days_published_before
    google_count = (shares['google'] if 'google' in shares else 0) / days_published_before
    pinterest_count = (shares['pinterest'] if 'pinterest' in shares else 0) / days_published_before
    linkdine_count = (shares['linkedin'] if 'linkedin' in shares else 0)/ days_published_before
    
    # no. of outgoing links in the article
    cr = start_link = article.text.find("a href")
    # no. of incoming sources of the article
    pr = 1 if reddit_count > 0 else 0 + \
        1 if facebook_count > 0 else 0 + \
        1 if google_count > 0 else 0 + \
        1 if pinterest_count > 0 else 0 + \
        1 if linkdine_count > 0 else 0 + 1
    first_cal = first_step_calculation(pr,cr)
    second_cal = second_step_calculation(reddit_count,facebook_count,google_count,pinterest_count,linkdine_count)
    third_cal = third_step_calculation(reddit_count,facebook_count,google_count,pinterest_count,linkdine_count)
    final_cal = (first_cal + second_cal + third_cal) 
    print final_cal
    return final_cal

def first_step_calculation(pr, cr):
    if cr > 0:
        return ((1 - devience) + (pr * devience)/cr)
    else : 
        return (1-devience)

def second_step_calculation(reddit_count,facebook_count,google_count,pinterest_count,linkdine_count):
    return (reddit_count * RDD_WT) + \
        (facebook_count * FB_WT) + \
        (google_count * GO_WT) + \
        (pinterest_count * PR_WT) + \
        (linkdine_count * LD_WT)

def third_step_calculation(reddit_count,facebook_count,google_count,pinterest_count,linkdine_count):
    max_count = max([reddit_count, facebook_count, google_count, pinterest_count, linkdine_count])
    if max_count > 0 :
        return (reddit_count/max_count) + (facebook_count/max_count) + \
            (google_count/max_count) + (pinterest_count/max_count) + \
            (linkdine_count/max_count)
    return 0

'''
To create url for pagination 
'''
def url_for_other_page(page):
    args = dict(request.args)
    args['page'] = page
    return url_for(request.endpoint, _external=True, **args)

'''
To hash the password
'''
def hash_password(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

'''
To hash the access-token
'''
def access_token():
    return bcrypt.hashpw(str(random.random()), bcrypt.gensalt())

'''
To validate/comapre the hash password
@param present - user's account present password
@param requested - password requested for verification
'''
def validate_hash_password(requested, present):
    return bcrypt.checkpw(str(requested), str(present))

'''
To generate unique code
uuid package
'''
def generate_unique_code():
    return uuid.uuid4()

'''
error message
'''
def error(message):
    return {
        'message' : message, 
        'tags' : 'error'
    }

'''
success message
'''
def success(message):
    return {
        'message' : message, 
        'tags' : 'success'
    }