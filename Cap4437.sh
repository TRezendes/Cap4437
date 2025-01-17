#!/bin/bash

# source /var/www/cap4437/.env
source .env

echo $token

curl https://kind.social/api/v1/statuses -H "Authorization: Bearer ${TOKEN}" -F "status=This is a text only test post via the Mastodon API."