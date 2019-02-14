from ..api.routes import app

from celery import Celery


def _make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = _make_celery(app)


@celery.task()
def on_commit(commit):
    payload = Payload(commit)

    try:
        if payload.get("deleted"):
            raise SkipUpdate("No update on tag deletion")

        try:
            tag = payload.tag
        except ValueError:
            raise SkipUpdate("Not a tag push")

        for matcher in config.matchers:
            if matcher.match(tag):
                break
        else:
            raise SkipUpdate("Tag {} does not match any spec".format(tag))

        update_package(payload.repository_name, payload.ssh_url, tag)

    except SkipUpdate as e:
        message = "Skipped package registration for {} ({!r})".format(
            payload.repository_name, e
        )
        status = 400

    except Exception as e:
        log.exception("Error processing commit message: %r", commit)
        message = "ERROR: Packge registration for {} failed ({!r})".format(
            payload.repository_name, e
        )
        status = 400
        notify_slack(config.slack_hook_url, message)

    else:
        message = "<{}|{}> of {} has been registered by {}".format(
            payload.tree_url, tag, payload.repository_name, payload.pusher_name
        )
        status = 200
        notify_slack(config.slack_hook_url, message)
    return status, message
