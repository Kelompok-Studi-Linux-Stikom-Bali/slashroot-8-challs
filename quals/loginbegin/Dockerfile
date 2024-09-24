# Gunakan image PHP sebagai basis
FROM php:8.2-apache

RUN docker-php-ext-install mysqli
RUN chmod 755 -R /var/www/html

# Create and Switch to a user called app
RUN useradd -ms /bin/bash app
USER app

COPY --chown=app:app . /var/www/html
# COPY ./config/php.ini /usr/local/etc/php/php.ini
