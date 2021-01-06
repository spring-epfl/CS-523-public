FROM debian:bullseye

# Identical parts between client and server.
# Add Tor repo and install necessary packages.
RUN \
apt-get update && \
apt-get install -y \
apt-utils \
apt-transport-https \
curl \
gnupg2 && \
curl -sSL https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --dearmor | tee /usr/share/keyrings/tor-archive-keyring.gpg >/dev/null && \
echo "deb [signed-by=/usr/share/keyrings/tor-archive-keyring.gpg] https://deb.torproject.org/torproject.org bullseye main" > /etc/apt/sources.list.d/tor.list && \
apt-get update && \
apt-get install -y \
deb.torproject.org-keyring \
locales \
procps \
python3-dev \
python3-pip \
runit \
tcpdump \
tor \
uwsgi \
uwsgi-plugin-python3

# UTF-8 support in console.
RUN \
printf '%s\n' 'fr_CH.UTF-8 UTF-8' 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && \
printf '%s\n' 'LANG="en_US.UTF-8"' 'LANGUAGE="en_US:en"' >> /etc/default/locale && \
dpkg-reconfigure --frontend=noninteractive locales && \
update-locale 'LANG=en_US.UTF-8' && \
echo "export VISIBLE=now" >> /etc/profile

# Python dependancies.
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# Client and server starts to differ here.

# Add server directory.
RUN mkdir -p /server

COPY ./etc /tmp/etc
RUN rm -r /etc/service /etc/tor && \
cp -R /tmp/etc/* /etc/ && \
chmod 755 /etc/tor && \
chmod 644 /etc/tor/torrc && \
chmod 755 -R /etc/service && \
rm -rf /tmp/etc

# Volume to store hidden service stuff.
VOLUME  ["/var/lib/tor/"]

# Volume containing code.
VOLUME  ["/server/"]

ENTRYPOINT ["runsvdir",  "-P", "/etc/service"]
