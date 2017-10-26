from flask import Flask, request, url_for

def url_for_other_page(page):
    args = dict(request.args)
    args['page'] = page
    return url_for(request.endpoint, _external=True, **args)
