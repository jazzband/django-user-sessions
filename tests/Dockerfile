FROM perl:latest

RUN cpanm MaxMind::DB::Writer

COPY generate_mmdb.pl /

VOLUME ["/data"]

CMD ["perl", "/generate_mmdb.pl"]
