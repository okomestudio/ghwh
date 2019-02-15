import os

env = os.environ


#: The Celery broker URL used by webhook.
webhook_celery_broker = env.get("WEBHOOK_CELERY_BROKER", "redis://localhost:6379")

#: The Celery backend used by webhook.
webhook_celery_backend = env.get("WEBHOOK_CELERY_BACKEND", "redis://localhost:6379")

#: The secret used for encoding GitHub commit message.
webhook_secret = env.get("WEBHOOK_SECRET")
