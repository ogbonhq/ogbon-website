# ogbon.com: the static site served by nginx on 127.0.0.1:8092 (nginx.conf). Built and pushed to
# ghcr.io/ogbonhq/ogbon-website:<branch> by CI; the web VM pulls :main (deploy/ogbon-web-update.sh).
FROM nginx:1.30.6-alpine

RUN rm -f /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html
RUN rm -f index.html 50x.html
COPY index.html compare.html research.html team.html 404.html \
     styles.css script.js compare.js vision.js \
     favicon.ico favicon.svg apple-touch-icon.png site.webmanifest robots.txt sitemap.xml ./
COPY assets/ assets/

# Not served: the updater copies these out of the image onto the VM.
COPY deploy/ /opt/ogbon-web/deploy/

ARG GIT_SHA=unknown
LABEL org.opencontainers.image.revision=$GIT_SHA
ENV NGINX_ENTRYPOINT_QUIET_LOGS=1
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --start-interval=1s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8092/ || exit 1
