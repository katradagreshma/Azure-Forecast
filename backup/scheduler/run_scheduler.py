import schedule
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from batch.batch_predict import run_batch_prediction


def scheduled_job():
    try:
        success = run_batch_prediction()
        pass
    except Exception as e:
        pass

if __name__ == "__main__":
    scheduled_job()

    schedule.every().day.at("02:00").do(scheduled_job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        pass
