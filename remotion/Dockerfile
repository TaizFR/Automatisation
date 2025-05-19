FROM node:22-bookworm-slim
WORKDIR /app
RUN apt-get update
RUN apt install -y \
  libnss3 \
  libdbus-1-3 \
  libatk1.0-0 \
  libgbm-dev \
  libasound2 \
  libxrandr2 \
  libxkbcommon-dev \
  libxfixes3 \
  libxcomposite1 \
  libxdamage1 \
  libatk-bridge2.0-0 \
  libpango-1.0-0 \
  libcairo2 \
  libcups2

COPY package*.json tsconfig.json* remotion.config.* ./
COPY ./remotion/src ./src
COPY ./remotion/public ./public
RUN npm ci
RUN npx remotion browser ensure
COPY render.mjs render.mjs
CMD ["node", "render.mjs"]