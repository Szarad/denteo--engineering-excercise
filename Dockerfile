FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
RUN groupadd -g 999 denteouser && \
    useradd --create-home -r -u 999 -g denteouser denteouser
USER denteouser
WORKDIR /home/denteouser
ENV PATH "$PATH:/home/denteouser/.local/bin"
ENV development_env local
ENV production_url docs
COPY --chown=denteouser:denteouser . .
ENV PORT 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
