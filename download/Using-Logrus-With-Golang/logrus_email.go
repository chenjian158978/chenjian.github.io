package main

import (
	"time"

	"github.com/logrus_mail"
	"github.com/sirupsen/logrus"
)

func main() {
	logger := logrus.New()
	hook, err := logrus_mail.NewMailAuthHook(
		"logrus_email",
		"smtp.gmail.com",
		587,
		"chenjian158978@gmail.com",
		"271802559@qq.com",
		"chenjian158978@gmail.com",
		"xxxxxxx",
	)
	if err == nil {
		logger.Hooks.Add(hook)
	}
	//生成*Entry
	var filename = "123.txt"
	contextLogger := logger.WithFields(logrus.Fields{
		"file":    filename,
		"content": "GG",
	})
	//设置时间戳和message
	contextLogger.Time = time.Now()
	contextLogger.Message = "这是一个hook发来的邮件"
	//只能发送Error,Fatal,Panic级别的log
	contextLogger.Level = logrus.ErrorLevel

	//使用Fire发送,包含时间戳，message
	hook.Fire(contextLogger)
}
