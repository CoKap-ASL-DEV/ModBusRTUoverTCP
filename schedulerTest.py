from datetime import datetime, timedelta
import schedule
import time



def job():
    today = datetime.now()  
    today_yymmdd_str = today.strftime('%Y-%m-%d %H:%M:%S')
    print(today_yymmdd_str)    
    

schedule.every(1).minutes.at(":00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
