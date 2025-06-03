docker-compose.exe -f .\compose_build.yml up --build


docker tag 4e1ab1beab9a registry.cn-hangzhou.aliyuncs.com/wjn0918/soft:easybd-frontend
docker push registry.cn-hangzhou.aliyuncs.com/wjn0918/soft:easybd-frontend
docker tag e45f6badeae5 registry.cn-hangzhou.aliyuncs.com/wjn0918/soft:easybd-backend
docker push registry.cn-hangzhou.aliyuncs.com/wjn0918/soft:easybd-backend