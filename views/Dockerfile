# Dockerfile for react frontend

# Use Node.js as the base image for frontend
FROM node:21-alpine

# Set the working directory for frontend
WORKDIR /app

# Copy all files and folders from the current directory into /app
COPY . /app

# Install dependencies and build the frontend
RUN npm install
RUN npm run build

# Expose the frontend port
EXPOSE 5173

# Start the React development server
CMD ["npm", "run", "dev"]