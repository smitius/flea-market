flea-market app

docker buildx create --use
docker buildx inspect --bootstrap

docker buildx build --platform linux/amd64,linux/arm64 \
  -t your_dockerhub_username/flea-market-app:latest \
  --push \
  .


version: '3.8'

services:
  flea-market:
    image: smintik/flea-market-app:latest
    ports:
      - "8111:5000"
    volumes:
      - uploads:/app/app/static/uploads
      - db:/app/instance/
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=somethingsomethingelse
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=sellingisfun
      - SITE_NAME=du kan skicka meddelanden till oss via BRF Bolinders Terrass-gruppen (Hana Pollak, Peter Smitka)
      - WHATSAPP_NUMBER=+46707447005
      - APARTMENT_ADDRESS=Vi bor i entré 11, våning -1, lägenhet 902
    restart: unless-stopped

volumes:
  uploads:
  db: