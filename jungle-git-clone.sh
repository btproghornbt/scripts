#!/bin/sh

user_email = "btproghornbt@protonmail.com"
user_name = "btproghornbt"
server = "github-proghorn"

url="$1"
[ -n "$2" ] && dir="$2" || (echo "insert dir to save";read dir)
changed_url=$(echo $url|sed s/github.com/$server/)

git clone $changed_url $dir
cd $dir
git config user.email $user_email
git config user.name  $user_name

