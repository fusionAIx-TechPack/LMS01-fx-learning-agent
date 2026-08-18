FROM php:8.3-apache-bookworm
ARG MOODLE_VERSION=5.0.3
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl default-mysql-client git libcurl4-openssl-dev libfreetype6-dev libicu-dev libjpeg62-turbo-dev libonig-dev libpng-dev libxml2-dev libzip-dev unzip \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j"$(nproc)" curl exif gd intl mbstring mysqli opcache soap zip \
    && curl -fsSL "https://github.com/moodle/moodle/archive/refs/tags/v${MOODLE_VERSION}.tar.gz" | tar -xz --strip-components=1 -C /var/www/html \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/www/moodledata \
    && chown -R www-data:www-data /var/www/html /var/www/moodledata
COPY config.php /var/www/html/config.php
COPY moodle.ini /usr/local/etc/php/conf.d/moodle.ini
COPY entrypoint.sh /usr/local/bin/moodle-entrypoint
RUN chmod +x /usr/local/bin/moodle-entrypoint
ENTRYPOINT ["moodle-entrypoint"]
CMD ["apache2-foreground"]
