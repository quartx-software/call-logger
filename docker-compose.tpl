version: "3.3"

volumes:
  calllogger-data:

services:
  app:
    image: "%%IMAGE_NAME%%:%%IMAGE_TAG%%"
    privileged: true
    restart: on-failure
    network_mode: host
    volumes:
      - type: volume
        source: calllogger-data
        target: /data
      - type: bind
        source: /dev
        target: /dev
    environment:
      DOMAIN: "https://quartx.dev/"
      DEBUG: "true"
