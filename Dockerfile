# Use the official MongoDB image as the base image
FROM mongo:latest

# Set the environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=fmigas
ENV MONGO_INITDB_ROOT_PASSWORD=fmigas123

# Expose the default MongoDB port
EXPOSE 27017

# Start the MongoDB service
CMD ["mongod"]
