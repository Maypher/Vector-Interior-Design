#!/bin/bash

runningPort=$PORT

if [ "$BUILD_TARGET" = 'dev' ]; then
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory --dev
else
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory
fi
