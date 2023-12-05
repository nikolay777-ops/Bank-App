#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

if [ $CELERY_TASK_ALWAYS_EAGER != True ]
then
  echo "Waiting for rabbitmq..."
  while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
    sleep 3;
  done
fi

exec "$@"
