# List available slots from the schedule

## Installation
### Docker:
1. Build a Docker image
```
docker build -t <DockerImageName>:<DockerImageReleaseTag>
```
2. Run the Docker image:
```
docker run --rm --name scheduler -p 8000:8000 <DockerImageName>:<DockerImageReleaseTag>
```
3. See and use the docs for the application under:
http://localhost:8000/docs

### Virtual environment:
1. Create the virtual environment:
```
python3 -m venv venv_<ProjectName>
```
2. activate virtual environment:
```
source venv_<ProjectName>/bin/activate
```
3. Install dependencies:
```
pip3 install -r requirements.txt
```
4. Run the application:
```
uvicorn app.main:app
```
5. See and use the docs for the application under:
http://localhost:8000/docs
