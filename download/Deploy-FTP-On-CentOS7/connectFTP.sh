#!/usr/bin/env bash

HOST=192.168.1.145
USER=chenjian
PASSWORD=chenjian
FILENAME=$1
LOCAL_PATH=/var/dfdfdf/
REMOTE_PATH=/home/dddd/
lftp -u ${USER},${PASSWORD} sftp://${HOST} << EOF
  lcd ${LOCAL_PATH}
  cd ${REMOTE_PATH}
  # 上传文件
  put ${FILENAME}

  # 下载文件
  get ${FILENAME}
  bye
EOF