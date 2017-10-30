from crontab import CronTab
import os
import getpass

feed_cron = CronTab(user=getpass.getuser())
job = feed_cron.new(command='cd ' + os.getcwd()+ ' && python manage.py cron > /tmp/cron.log')
job.minute.every(1)
 
feed_cron.write()