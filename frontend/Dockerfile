FROM nginx:alpine

# Copy the frontend files to the default Nginx html directory
COPY ./ /usr/share/nginx/html/

# Copy the custom Nginx config to proxy API requests to the backend
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
