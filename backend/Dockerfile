FROM node:14.16-alpine3.13
WORKDIR /work
EXPOSE 3000
COPY package.json package-lock.json app.js prh.yml .textlintrc /work/
RUN npm install
CMD ["node", "app.js"]