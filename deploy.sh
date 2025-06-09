docker buildx build --platform linux/amd64 -t bloodbloy/roadflow-api . --no-cache

 docker tag bloodbloy/roadflow-api northamerica-south1-docker.pkg.dev/manifest-grin-462423-m3/flow-images/flow-api:latest

 docker push  northamerica-south1-docker.pkg.dev/manifest-grin-462423-m3/flow-images/flow-api:latest

 gcloud run deploy flow-api --image northamerica-south1-docker.pkg.dev/manifest-grin-462423-m3/flow-images/flow-api:latest --region northamerica-south1 --allow-unauthenticated --env-vars-file .env.yaml --memory 2Gi --cpu 2