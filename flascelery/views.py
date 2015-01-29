"""
Flask views

"""
# ============================================================================
# necessary imports
# ============================================================================
from flask import session, request, render_template, flash, jsonify, url_for
from flask import redirect
from flask.ext.mail import Message

from flascelery import app
from flascelery.tasks import send_async_email, long_task


# ============================================================================
# views
# ============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    """Index view"""
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the mail
    msg = Message('Hello from Flask', recipients=[request.form['email']])
    msg.body = 'This is a test email sent from a background Celery task'

    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(msg)
        flash('Sending email to {}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60)
        flash('An email will be sent to {} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    """
    Route for starting long background task.

    """
    task = long_task.apply_async()

    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    """Celery task status notifier."""
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job has not started yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending..'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this's the exception raised
        }

    return jsonify(response)
# ============================================================================
# EOF
# ============================================================================
