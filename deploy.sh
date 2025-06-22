
REGION="us-west1"
PROJECT_ID="manifest-grin-462423-m3"
REPO_NAME="hackaton"

docker buildx build --platform linux/amd64 -t bloodbloy/roadflow-api . --no-cache

 docker tag bloodbloy/roadflow-api ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/flow-api:latest

 docker push  ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/flow-api:latest

 gcloud run deploy flow-api --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/flow-api:latest --region ${REGION} --allow-unauthenticated --env-vars-file .env.yaml --memory 2Gi --cpu 2