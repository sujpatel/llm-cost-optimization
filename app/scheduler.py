from apscheduler.schedulers.background import BackgroundScheduler

from app.sync_models import sync_models
from app.sync_benchmarks import sync_benchmarks


def run_sync_jobs():
    sync_models()
    sync_benchmarks()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_sync_jobs, "interval", hours=6)
    scheduler.start()
    return scheduler
