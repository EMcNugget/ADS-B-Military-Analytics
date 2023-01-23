FROM ubuntu:latest

WORKDIR C:/Users/ethan/OneDrive/Desktop/adsb_mil_data

ENV PORT=8080

EXPOSE 8080

CMD ["auto_req.py"]