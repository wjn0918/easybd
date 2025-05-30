# 生产阶段
FROM nginx:stable-alpine

# 拷贝构建结果
COPY dist/ /usr/share/nginx/html/

# 使用自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
