FROM alpine:3.21
WORKDIR /app
COPY wtl_proxy /app/wtl_proxy
COPY label_templates /app/templates
ENV PYTHONUNBUFFERED=1
RUN apk add --no-cache python3 py3-aiohttp

EXPOSE 8985
CMD [ "python3", "-m", "wtl_proxy"]
