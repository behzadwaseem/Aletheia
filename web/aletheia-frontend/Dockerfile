FROM node:18-alpine

WORKDIR /app

# Install deps
COPY package.json package-lock.json* ./
RUN npm install

# Copy source
COPY . .

# Build Next.js
RUN npm run build

# Expose frontend port
EXPOSE 3000

# Start Next.js
CMD ["npm", "run", "start"]
