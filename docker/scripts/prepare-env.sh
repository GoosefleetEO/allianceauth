#!/bin/bash
set -e
FILE=./.env
if test -f "$FILE"; then
    echo "$FILE exists. If you wish to recreate your auth environment variables (which will break everything), delete the .env file."
    exit;
fi
cp .env.example .env

# Autogenerate 24 character hexadecimal strings for all passwords + secret key
sed -i.bak 's/%PROXY_MYSQL_PASS%/'"$(openssl rand -hex 24)"'/g' .env
sed -i.bak 's/%PROXY_MYSQL_PASS_ROOT%/'"$(openssl rand -hex 24)"'/g' .env
sed -i.bak 's/%GRAFANA_DB_PASSWORD%/'"$(openssl rand -hex 24)"'/g' .env
sed -i.bak 's/%AA_SECRET_KEY%/'"$(openssl rand -hex 24)"'/g' .env
sed -i.bak 's/%AA_DB_PASSWORD%/'"$(openssl rand -hex 24)"'/g' .env
sed -i.bak 's/%AA_DB_ROOT_PASSWORD%/'"$(openssl rand -hex 24)"'/g' .env

#Prompts to collect user information
IFS= read -p "Enter the display name for your auth instance: " sitename
sed -i.bak 's/%AA_SITENAME%/'\""${sitename}"\"'/g' .env

read -p "Enter the base domain: " domain
sed -i.bak 's/%DOMAIN%/'${domain}'/g' .env

read -p "Enter the subdomain for auth: " subdomain
sed -i.bak 's/%AUTH_SUBDOMAIN%/'${subdomain}'/g' .env

read -p "Enter an email address. This is requested by CCP if there are any issues with your ESI application, and is not used in any other way by AllianceAuth: " email
sed -i.bak 's/%ESI_USER_CONTACT_EMAIL%/'${email}'/g' .env

echo "Visit https://developers.eveonline.com/ and create an application with the callback url https://${subdomain}.${domain}/sso/callback"

read -p "Enter ESI Client ID: " clientid
sed -i.bak 's/%ESI_SSO_CLIENT_ID%/'${clientid}'/g' .env

read -p "Enter ESI Client Secret: " clientsecret
sed -i.bak 's/%ESI_SSO_CLIENT_SECRET%/'${clientsecret}'/g' .env

source ./.env
cp setup.base.sql setup.sql

# Create init SQL file for auth database with users
sed -i.bak 's/authpass/'"$AA_DB_PASSWORD"'/g' setup.sql
sed -i.bak 's/grafanapass/'"$GRAFANA_DB_PASSWORD"'/g' setup.sql
rm *.bak
rm .env.bak
