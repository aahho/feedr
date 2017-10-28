from crontab import CronTab
import os
import getpass

feed_cron = CronTab(user=getpass.getuser())
job = feed_cron.new(command='cd ' + os.getcwd()+ ' | python manage.py cron')
job.minute.every(30)
 
feed_cron.write()