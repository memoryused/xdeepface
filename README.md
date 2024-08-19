## :nut_and_bolt: Development 
#### Clone project
- git clone  -b <branch_name>
- cd to your local directory

#### Create env and activate
- conda env create -f environment.yml
- conda activate <env_name> # ที่ระบุชื่อเอาไว้ในไฟล์ environment.yml

#### Install requirement
- pip install --no-cache-dir -r requirements.txt

#### Start app
- python .\app.py

## :notebook: Deployment
#### Create docker image 
- docker build -f Dockerfile -t regis.dev.sit/chatbot/deepface-dev:0.0.1 . --no-cache

#### Test run on my docker
- docker run -p 5001:5001 -it --name xdeepface regis.dev.sit/chatbot/deepface-dev:0.0.1

#### Push image to registry (habor)
- docker push regis.dev.sit/chatbot/deepface-dev:0.0.1

#### Putty to server (Must action with root)
- tmux a 

#### Pull and Run docker
- docker pull regis.dev.sit/chatbot/deepface-dev@sha256:01e30a5f3aca638dfd30d35140c1a7084763d63422f41b87ecc0254dbcd8609c
- docker run -p 5001:5001 -it --name xdeepface regis.dev.sit/chatbot/deepface-dev:0.0.1