import socialshares
import datetime

class DuckRank:
    FACEBOOK_WEIGHTAGE = 0.2
    LINKEDIN_WEIGHTAGE = 0.4
    PINTEREST_WEIGHTAGE = 0.3
    REDDIT_WEIGHTAGE = 0.6
    GOOGLE_WEIGHTAGE = 0.7
    DEVIANCE = 0.85
    GRAVITY_CONST = 1.8

    def __init__(self, url, article, alexa_rank, published_at):
        self.url = url
        self.article = article
        self.alexa_rank = alexa_rank  
        self.published_at = published_at
        self.shares = {}

        self.set_article_age()
        self.set_social_media_share_counts()
        self.set_pr()
        self.set_cr()

    def set_article_age(self):
        self.article_age = (datetime.datetime.now() - self.published_at).days \
            if (datetime.datetime.now() - self.published_at).days > 0 else 1

    def set_social_media_share_counts(self):
        shares = socialshares.fetch(self.url, ['facebook', 'pinterest', 'google', 'linkedin', 'reddit'])

        self.shares['reddit'] = (shares['reddit']['ups'] if 'reddit' in shares else 0) 
        self.shares['facebook'] = (shares['facebook']['share_count'] if 'facebook' in shares else 0) 
        self.shares['google'] = (shares['google'] if 'google' in shares else 0) 
        self.shares['pinterest'] = (shares['pinterest'] if 'pinterest' in shares else 0) 
        self.shares['linkedin'] = (shares['linkedin'] if 'linkedin' in shares else 0) 

    # no. of incoming sources of the article
    def set_pr(self):
        self.pr = sum([1 if value > 0 else 0 for value in self.shares.values()]) + 1

    # no. of outgoing links in the article
    def set_cr(self):
        self.cr = self.start_link = self.article.text.find("a href")

    '''
    algo for duck rank calculation
    '''
    def calculate(self):
        return self.first_step_calculation() + \
        (self.second_step_calculation() / (self.alexa_rank * ((self.article_age + 2)**self.GRAVITY_CONST)))

    def first_step_calculation(self):
        if self.cr > 0:
            return ((1 - self.DEVIANCE) + (self.pr * self.DEVIANCE) / self.cr)
        else : 
            return 1 - self.DEVIANCE

    def second_step_calculation(self):
        return (self.shares['reddit'] * self.REDDIT_WEIGHTAGE) + \
            (self.shares['facebook'] * self.FACEBOOK_WEIGHTAGE) + \
            (self.shares['google'] * self.GOOGLE_WEIGHTAGE) + \
            (self.shares['pinterest'] * self.PINTEREST_WEIGHTAGE) + \
            (self.shares['linkedin'] * self.LINKEDIN_WEIGHTAGE) + 1

    # def third_step_calculation(self):
    #     max_count = max(self.shares.values())
    #     if max_count > 0 :
    #         return (self.shares['reddit'] / max_count) + (self.shares['facebook'] / max_count) + \
    #             (self.shares['google'] / max_count) + (self.shares['google'] / max_count) + \
    #             (self.shares['linkedin'] / max_count)
    #     return 0