package main

import (
	"os/exec"
	"strings"

	"github.com/gin-gonic/gin"
)

type IP struct {
	Address string `json:"address"`
}

// Function to sanitize input by removing special characters and common dangerous commands
func sanitizeInput(input string) string {
	// Blacklist of special characters
	specialChars := []string{"&", "|", "<", ">", "`", "'", "\"", " ", "@", "%", "^", "~"}
	for _, char := range specialChars {
		input = strings.ReplaceAll(input, char, "")
	}

	// Blacklist of dangerous commands
	blacklistCommands := []string{"ls", "cat", "tail", "more", "whoami", "pwd", "busybox", "echo"}
	for _, cmd := range blacklistCommands {
		input = strings.ReplaceAll(input, cmd, "")
	}

	return input
}

func main() {
	r := gin.Default()

	r.LoadHTMLGlob("template/*")

	r.GET("/", func(c *gin.Context) {
		c.HTML(200, "index.html", nil)
	})

	r.POST("/api/ping", func(c *gin.Context) {
		var param IP
		if err := c.Bind(&param); err != nil {
			c.JSON(400, gin.H{"message": "Invalid parameter"})
			return
		}

		// Sanitize the input to prevent injection attacks
		param.Address = sanitizeInput(param.Address)

		// Ping command with sanitized input
		commnd := "ping -c 1 -W 1 " + param.Address + " 1>&2"
		result, _ := exec.Command("sh", "-c", commnd).CombinedOutput()

		c.JSON(200, gin.H{
			"result": string(result),
		})
	})

	if err := r.Run(); err != nil {
		panic(err)
	}
}
