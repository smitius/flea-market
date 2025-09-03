flea-market app


git:

3405  git init
3406  git add .
3407  git commit -m "first commit"
3408  git remote add origin git@github.com:smitius/flea-market.git
3409  git branch -M main
3410  git push -u origin main

python version:

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