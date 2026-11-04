# RentEase — PHP 8 + Apache
#
# Render has no native PHP runtime, so the app ships as a container.
# pdo_sqlite lets the app self-initialise a database on a host with no MySQL.
FROM php:8.3-apache

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsqlite3-dev \
    && docker-php-ext-install pdo_mysql pdo_sqlite \
    && rm -rf /var/lib/apt/lists/*

# Apache serves /var/www/html; allow .htaccess-free pretty defaults
RUN a2enmod rewrite headers

COPY . /var/www/html/

# the SQLite file is created on first request, so this dir must be writable
RUN mkdir -p /var/www/html/database \
    && chown -R www-data:www-data /var/www/html/database \
    && chmod -R 775 /var/www/html/database

EXPOSE 80
