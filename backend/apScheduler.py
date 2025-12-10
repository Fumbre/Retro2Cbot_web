import threading
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger 
from functools import wraps

class SchedulerTool:
    _instance = None  ## create the only singleton viarable 

    ##  singleton mode function to create a single instance
    def __new__(cls): ## cls represent SchedulerTool class
        """
        Docstring for __new__
        create a SchedulerTool instance
        :author: Sunny
        :date: 09-12-2025
        :param cls: SchedulerTool class
        :return: scheduler instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls) # create SchedulerTool object
            cls._instance._init_scheduler() # generate instance 
        return cls._instance
    
    def _init_scheduler(self):
        """
        Docstring for _init_scheduler (create properties)
        :author: Sunny
        :date: 09-12-2025
        :param self: ScheduleTool instance
        :return: None
        """
        self.scheduler = BackgroundScheduler() 
        self.lock = threading.Lock()
        self.jobs = {}
        self.scheduler.start()

    def add_interval_job(self,func,seconds,job_id=None,args=None,kwargs=None):
        with self.lock:
            trigger = IntervalTrigger(seconds = seconds)
            job = self.scheduler.add_job(func,trigger,args=args,kwargs=kwargs,id=job_id)
            if job_id:
                self.jobs[job_id] = job
            return job

    def add_cron_job(self,func,corn_expression,job_id=None,args=None,kwargs=None):
        with self.lock:
            fields = corn_expression.split()
            if(len(fields) != 5):
                raise ValueError("Invalid corn expression!")
            minute, hour, day, month, day_of_week = fields
            trigger = CronTrigger(minute=minute,hour=hour,day=day,month=month,day_of_week = day_of_week)
            job = self.scheduler.add_job(func,trigger,args=args,kwargs=kwargs,id=job_id)
            if job_id:
                self.jobs[job_id] = job
            return job

    def remove_job(self,job_id):
        with self.lock:
            if job_id in self.jobs:
                self.scheduler.remove_job(job_id)
                self.jobs.pop(job_id,None)
    
    def shutdown(self):
        self.scheduler.shutdown()

    def lists_job(self):
        return self.scheduler.get_jobs()


def scheduled(interval=None,cron=None,job_id=None,args=None,kwargs=None):
    def decorator(func):
        sched = SchedulerTool()
        if interval:
            sched.add_interval_job(func, seconds=interval, job_id=job_id, args=args, kwargs=kwargs)
        elif cron:
            sched.add_cron_job(func, cron_expr=cron, job_id=job_id, args=args, kwargs=kwargs)
        else:
            raise ValueError("must point interval or cron")  

        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            return func(*f_args, **f_kwargs)
        return wrapper
    return decorator  
