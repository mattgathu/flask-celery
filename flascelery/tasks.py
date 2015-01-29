"""
Celery Async tasks definitions

"""
# ============================================================================
# necessary imports
# ============================================================================
import random
import time

import celery

from flascelery import app, mail


# ============================================================================
# tasks defintions
# ============================================================================
@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        print('sending mail')
        mail.send(msg)


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmoinc', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']

    message = ''

    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{} {} {}'.format(random.choice(verb),
                                        random.choice(adjective),
                                        random.choice(noun))

        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})

        time.sleep(1)

    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}
# ============================================================================
# EOF
# ============================================================================
