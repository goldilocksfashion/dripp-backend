package websocket

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

// Server is an interface that defines the behavior of a WebSocket server.
type Server interface {
	StartServer(port string)
	AddHandler(handler HandlerFunc)
}

type HandlerFunc func(*websocket.Conn, *websocket.Message)

type Message struct {
	MessageType int
	Data        []byte
}

type serverImpl struct {
	upgrader websocket.Upgrader
	handlers []HandlerFunc
}

func NewServer() Server {
	return &serverImpl{
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
		},
	}
}

// StartServer starts the WebSocket server on the specified port.
func (s *serverImpl) StartServer(port string) {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		conn, err := s.upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Println(err)
			return
		}
		defer conn.Close()

		for _, handler := range s.handlers {
			go s.handleConnection(conn, handler)
		}
	})

	log.Fatal(http.ListenAndServe(":"+port, nil))
}

// AddHandler adds a message handler to the WebSocket server.
// Libraries can use this method to add their own custom message handling logic.
func (s *serverImpl) AddHandler(handler MessageHandler) {
	s.handlers = append(s.handlers, handler)
}

func (s *serverImpl) handleConnection(conn *websocket.Conn, handler HandlerFunc) {
	for {
		messageType, data, err := conn.ReadMessage()
		if err != nil {
			log.Println(err)
			break
		}
		handler(conn, &Message{MessageType: messageType, Data: data})
	}
}

func (s *serverImpl) AddHandler(handler HandlerFunc) {
	s.handlers = append(s.handlers, handler)
}