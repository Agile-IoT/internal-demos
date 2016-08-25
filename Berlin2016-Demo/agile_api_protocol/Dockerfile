FROM resin/raspberrypi2-debian:jessie

# Install dependencies
RUN apt-get clean && apt-get update && apt-get install -y \
  python3-dbus

RUN apt-get clean && apt-get update && apt-get install -y \
  libdbus-1-dev \
  libdbus-glib-1-dev \
  python3-gi

RUN apt-get clean && apt-get update && apt-get install -y \
  python3-pip

RUN apt-get clean && apt-get update && apt-get install -y \
  build-essential

RUN apt-get clean && apt-get update && apt-get install -y \
  python3-dev

RUN apt-get clean && apt-get update && apt-get install -y \
  python3-tk

# resin-sync will always sync to /usr/src/app, so code needs to be here.
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY dbus_server dbus_server
COPY ge_link_bulb ge_link_bulb
COPY start.sh start.sh

CMD [ "bash", "/usr/src/app/start.sh" ]
